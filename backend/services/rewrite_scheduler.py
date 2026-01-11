from sqlalchemy.orm import Session
from models import Article
from services.rewrite_engine import rewrite_article_content


def run_rewrite_cycle(db: Session, limit: int = 3):
    """
    Rewrite limited number of old / weak articles
    """
    articles = (
        db.query(Article)
        .filter(Article.status == "published")
        .order_by(Article.view_count.asc())
        .limit(limit)
        .all()
    )

    rewritten = 0

    for article in articles:
        success = rewrite_article_content(db, article.id)
        if success:
            rewritten += 1

    return rewritten
