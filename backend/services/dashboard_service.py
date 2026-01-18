from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from models import Article
from models_trend_memory import TrendMemory

# CTR rules (same as ctr_optimizer)
WEAK_VIEW_THRESHOLD = 50
MAX_REWRITE_LIMIT = 2
GRACE_PERIOD_HOURS = 24


# =========================
# INTERNAL HELPER
# =========================

def _get_ctr_status(article: Article) -> str:
    """
    Returns CTR status for dashboard
    """

    if article.status != "published" or not article.published_at:
        return "draft"

    age = datetime.utcnow() - article.published_at

    if article.rewrite_count >= MAX_REWRITE_LIMIT:
        return "maxed"

    if age < timedelta(hours=GRACE_PERIOD_HOURS):
        return "cooldown"

    if article.view_count < WEAK_VIEW_THRESHOLD:
        return "weak"

    return "healthy"


# =========================
# DASHBOARD APIs
# =========================

def get_overview_stats(db: Session):
    total = db.query(Article).count()
    published = db.query(Article).filter(Article.status == "published").count()
    drafts = total - published

    weak_ctr = (
        db.query(Article)
        .filter(Article.status == "published")
        .filter(Article.view_count < WEAK_VIEW_THRESHOLD)
        .count()
    )

    return {
        "total_articles": total,
        "published_articles": published,
        "draft_articles": drafts,
        "weak_ctr_articles": weak_ctr
    }


def get_low_view_articles(db: Session, limit: int = 5):
    articles = (
        db.query(Article)
        .filter(Article.status == "published")
        .order_by(Article.view_count.asc())
        .limit(limit)
        .all()
    )

    return [
        {
            "id": a.id,
            "title": a.title,
            "views": a.view_count,
            "rewrite_count": a.rewrite_count,
            "ctr_status": _get_ctr_status(a)
        }
        for a in articles
    ]


def get_top_articles(db: Session, limit: int = 5):
    articles = (
        db.query(Article)
        .filter(Article.status == "published")
        .order_by(Article.view_count.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "id": a.id,
            "title": a.title,
            "views": a.view_count,
            "ctr_status": _get_ctr_status(a)
        }
        for a in articles
    ]


def get_trending_memory_stats(db: Session, limit: int = 5):
    records = (
        db.query(TrendMemory)
        .order_by(TrendMemory.times_used.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "topic": r.topic,
            "times_used": r.times_used,
            "last_used_at": r.last_used_at
        }
        for r in records
    ]
