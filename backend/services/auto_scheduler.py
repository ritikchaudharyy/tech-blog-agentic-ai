from sqlalchemy.orm import Session
from models import Article
from datetime import datetime


def pick_best_article_to_publish(db: Session):
    return (
        db.query(Article)
        .filter(
            Article.status == "approved",
            Article.is_deleted == False,
            Article.auto_publish == True
        )
        .order_by(
            Article.rewrite_count.desc(),
            Article.created_at.asc()
        )
        .first()
    )
