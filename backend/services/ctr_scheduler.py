from sqlalchemy.orm import Session
from models import Article
from services.ctr_optimizer import optimize_article_ctr


def run_ctr_optimization_cycle(db: Session, limit: int = 5):
    """
    Optimize CTR for limited number of weak articles
    """
    articles = (
        db.query(Article)
        .filter(Article.status == "published")
        .order_by(Article.view_count.asc())
        .limit(limit)
        .all()
    )

    optimized = 0

    for article in articles:
        success = optimize_article_ctr(db, article.id)
        if success:
            optimized += 1

    return optimized
