from datetime import datetime
from sqlalchemy.orm import Session

from backend.models import Article
from backend.models_trend_memory import TrendMemory


def _article_age_days(article: Article) -> int:
    if not article.published_at:
        return 1
    days = (datetime.utcnow() - article.published_at).days
    return max(days, 1)


# =========================
# OVERVIEW
# =========================

def get_overview_stats(db: Session):
    total = db.query(Article).count()
    published = db.query(Article).filter(Article.status == "published").count()
    drafts = total - published

    return {
        "total_articles": total,
        "published_articles": published,
        "draft_articles": drafts
    }


# =========================
# LOW VIEW ARTICLES
# =========================

def get_low_view_articles(db: Session, limit: int = 5):
    articles = (
        db.query(Article)
        .filter(Article.status == "published")
        .order_by(Article.view_count.asc())
        .limit(limit)
        .all()
    )

    results = []
    for a in articles:
        age_days = _article_age_days(a)
        velocity = round(a.view_count / age_days, 2)

        results.append({
            "id": a.id,
            "title": a.title,
            "views": a.view_count,
            "views_per_day": velocity,
            "rewrite_count": a.rewrite_count
        })

    return results


# =========================
# TOP ARTICLES
# =========================

def get_top_articles(db: Session, limit: int = 5):
    articles = (
        db.query(Article)
        .filter(Article.status == "published")
        .order_by(Article.view_count.desc())
        .limit(limit)
        .all()
    )

    results = []
    for a in articles:
        age_days = _article_age_days(a)
        velocity = round(a.view_count / age_days, 2)
        predicted = int(velocity * 7)

        results.append({
            "id": a.id,
            "title": a.title,
            "views": a.view_count,
            "views_per_day": velocity,
            "predicted_next_7_days": predicted
        })

    return results


# =========================
# TRENDING MEMORY
# =========================

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


# =========================
# VIEW TRENDS (NEW)
# =========================

def get_view_trends(db: Session, limit: int = 10):
    """
    Velocity-based trend analysis
    """

    articles = (
        db.query(Article)
        .filter(Article.status == "published")
        .all()
    )

    trends = []
    for a in articles:
        age_days = _article_age_days(a)
        velocity = round(a.view_count / age_days, 2)

        trends.append({
            "id": a.id,
            "title": a.title,
            "views": a.view_count,
            "views_per_day": velocity
        })

    # Sort by velocity (fastest growing)
    trends.sort(key=lambda x: x["views_per_day"], reverse=True)

    return trends[:limit]
