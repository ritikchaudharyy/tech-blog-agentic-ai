from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models import Article
from services.agentic_brain import generate_canonical_article


MIN_DAYS_OLD = 30
MAX_REWRITE_LIMIT = 2
LOW_VIEW_THRESHOLD = 100


def is_rewrite_eligible(article: Article) -> bool:
    """
    Decide if article should be rewritten
    """
    if article.rewrite_count >= MAX_REWRITE_LIMIT:
        return False

    if article.view_count >= LOW_VIEW_THRESHOLD:
        return False

    if not article.published_at:
        return False

    age = datetime.utcnow() - article.published_at
    if age < timedelta(days=MIN_DAYS_OLD):
        return False

    return True


def rewrite_article_content(db: Session, article_id: int) -> bool:
    """
    AI-powered content rewrite pipeline
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        return False

    if not is_rewrite_eligible(article):
        return False

    prompt = f"""
    Rewrite the following blog article to improve:
    - Clarity
    - Freshness
    - SEO
    - Readability

    Rules:
    - Keep original meaning
    - Do not change topic
    - No keyword stuffing
    - Professional tone
    - Add updated insights if relevant

    Title:
    {article.title}

    Content:
    {article.canonical_content}
    """

    rewritten = generate_canonical_article(prompt)

    if not rewritten or "content" not in rewritten:
        return False

    article.canonical_content = rewritten["content"]
    article.rewrite_count += 1
    article.last_optimized_at = datetime.utcnow()

    db.commit()
    return True
