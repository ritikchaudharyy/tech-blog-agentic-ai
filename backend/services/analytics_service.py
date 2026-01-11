from sqlalchemy.orm import Session
from datetime import datetime
from models import Article


def register_article_view(db: Session, article_id: int):
    """
    Increment view count for an article
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        return

    article.view_count += 1
    db.commit()


def mark_article_optimized(db: Session, article_id: int):
    """
    Mark article as optimized / rewritten by AI
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        return

    article.rewrite_count += 1
    article.last_optimized_at = datetime.utcnow()
    db.commit()
