from sqlalchemy.orm import Session
from backend.models import Article
from backend.models_trend_memory import TrendMemory

def get_overview_stats(db: Session):
    total = db.query(Article).count()
    published = db.query(Article).filter(Article.status == "published").count()
    drafts = db.query(Article).filter(Article.status != "published").count()

    return {
        "total_articles": total,
        "published_articles": published,
        "draft_articles": drafts
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
            "rewrite_count": a.rewrite_count
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
            "views": a.view_count
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
