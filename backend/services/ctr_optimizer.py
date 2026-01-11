from sqlalchemy.orm import Session
from models import Article
from services.agentic_brain import generate_canonical_article


WEAK_VIEW_THRESHOLD = 50
MAX_REWRITE_LIMIT = 2


def is_ctr_weak(article: Article) -> bool:
    """
    Decide if article needs CTR optimization
    """
    if article.view_count >= WEAK_VIEW_THRESHOLD:
        return False

    if article.rewrite_count >= MAX_REWRITE_LIMIT:
        return False

    if not article.seo_title or len(article.seo_title) < 40:
        return True

    return True


def generate_ctr_optimized_seo(article: Article) -> dict:
    """
    Generate better SEO title & meta description
    """
    prompt = f"""
    Improve the SEO title and meta description for higher click-through rate.

    Rules:
    - Title max 60 characters
    - Meta description max 155 characters
    - Professional, curiosity-driven
    - No clickbait
    - Topic: {article.title}

    Content:
    {article.canonical_content[:1500]}
    """

    result = generate_canonical_article(prompt)

    return {
        "seo_title": result.get("seo_title", article.seo_title),
        "meta_description": result.get(
            "meta_description",
            article.meta_description
        )
    }


def optimize_article_ctr(db: Session, article_id: int) -> bool:
    """
    Main CTR optimization pipeline
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        return False

    if not is_ctr_weak(article):
        return False

    seo_data = generate_ctr_optimized_seo(article)

    article.seo_title = seo_data["seo_title"]
    article.meta_description = seo_data["meta_description"]
    article.rewrite_count += 1

    db.commit()
    return True
