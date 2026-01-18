from sqlalchemy.orm import Session
import logging
from datetime import datetime, timedelta

from database import SessionLocal
from models import Article
from services.ctr_optimizer import optimize_article_ctr

logger = logging.getLogger(__name__)

CTR_CHECK_DELAY_HOURS = 24


def run_ctr_optimization():
    """
    Runs CTR optimization for eligible published articles
    """
    db: Session = SessionLocal()
    optimized_count = 0
    failed_count = 0

    try:
        logger.info("🚀 CTR optimization job started")

        cutoff_time = datetime.utcnow() - timedelta(hours=CTR_CHECK_DELAY_HOURS)

        articles = (
            db.query(Article)
            .filter(Article.status == "published")
            .filter(Article.published_at <= cutoff_time)
            .all()
        )

        logger.info(f"Found {len(articles)} eligible articles for CTR optimization")

        for article in articles:
            try:
                success = optimize_article_ctr(db, article.id)

                if success:
                    optimized_count += 1
                    logger.info(f"✅ CTR optimized for article ID {article.id}")
                else:
                    logger.warning(f"⚠️ CTR optimization skipped for article ID {article.id}")

            except Exception as article_error:
                failed_count += 1
                db.rollback()
                logger.exception(
                    f"❌ CTR optimization failed for article ID {article.id}: {article_error}"
                )

        logger.info(
            f"🎯 CTR optimization job completed | "
            f"Optimized: {optimized_count}, Failed: {failed_count}"
        )

    except Exception as e:
        db.rollback()
        logger.exception("🔥 CTR scheduler job failed unexpectedly")

    finally:
        db.close()
