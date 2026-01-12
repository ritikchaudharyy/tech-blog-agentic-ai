from sqlalchemy.orm import Session
import logging
from datetime import datetime, timedelta

from backend.database import SessionLocal
from backend.models import Article
from backend.services.ctr_optimizer import optimize_article_ctr

logger = logging.getLogger(__name__)

CTR_CHECK_DELAY_HOURS = 24


def run_ctr_optimization():
    """
    Runs CTR optimization for eligible articles
    """
    db: Session = SessionLocal()
    try:
        logger.info("CTR optimization job started")

        cutoff_time = datetime.utcnow() - timedelta(hours=CTR_CHECK_DELAY_HOURS)

        articles = (
            db.query(Article)
            .filter(Article.status == "published")
            .filter(Article.published_at <= cutoff_time)
            .all()
        )

        optimized_count = 0

        for article in articles:
            success = optimize_article_ctr(db, article.id)
            if success:
                optimized_count += 1
                logger.info(f"CTR optimized for article ID {article.id}")

        logger.info(f"CTR job completed. Optimized {optimized_count} articles.")

    except Exception as e:
        logger.exception("CTR scheduler job failed")

    finally:
        db.close()
