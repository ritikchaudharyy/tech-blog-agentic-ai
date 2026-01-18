from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import logging

from database import SessionLocal
from models import Article
from services.trending_agent import get_trending_topics
from services.prompt_loader import load_master_prompt
from services.agentic_brain import generate_canonical_article
from services.publishers.blogger import BloggerPublisher
from services.scheduler_state import AUTO_PUBLISH_ENABLED
from services.ctr_scheduler import run_ctr_optimization


# =========================
# LOGGING
# =========================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def daily_auto_publish():
    """
    Runs once per day.
    Picks a trending topic, generates an article,
    and publishes it to Blogger if auto-publish is enabled.
    """

    if not AUTO_PUBLISH_ENABLED:
        logger.info("Auto publish is paused. Job skipped.")
        return

    db = SessionLocal()

    try:
        logger.info("Daily auto publish job started")

        # Step 1: Load master prompt & trending topic
        master_prompt = load_master_prompt()
        topics = get_trending_topics(
            master_prompt=master_prompt,
            region="global",
            limit=1
        )

        if not topics:
            logger.warning("No trending topics found. Job aborted.")
            return

        topic = topics[0]

        # Step 2: Generate canonical article
        content = generate_canonical_article(
            master_prompt=master_prompt,
            user_topic=topic
        )

        if not content:
            logger.error("AI content generation failed. Job aborted.")
            return

        # Step 3: Save article
        article = Article(
            title=topic,
            canonical_content=content,
            platform_target="blogger",
            status="approved",
            created_at=datetime.utcnow()
        )

        db.add(article)
        db.commit()
        db.refresh(article)

        # Step 4: Publish to Blogger
        publisher = BloggerPublisher()
        result = publisher.publish(article)

        article.status = "published"
        article.published_at = datetime.utcnow()
        db.commit()

        logger.info("Article auto-published successfully")
        logger.info(f"Published URL: {result.get('url')}")

    except Exception:
        logger.exception("Auto publish job failed")

    finally:
        db.close()


def start_scheduler():
    """
    Starts background scheduler.
    - Auto publish: 09:00 AM
    - CTR optimization: 02:00 AM
    """

    scheduler = BackgroundScheduler()

    # 🔹 Daily auto publish (09:00 AM)
    scheduler.add_job(
        daily_auto_publish,
        trigger="cron",
        hour=9,
        minute=0,
        id="daily_auto_publish_job",
        replace_existing=True
    )

    # 🔹 Daily CTR optimization (02:00 AM)
    scheduler.add_job(
        run_ctr_optimization,
        trigger="cron",
        hour=2,
        minute=0,
        id="daily_ctr_optimization_job",
        replace_existing=True
    )

    scheduler.start()
    logger.info(
        "Scheduler started. Auto publish + CTR optimization jobs registered."
    )
