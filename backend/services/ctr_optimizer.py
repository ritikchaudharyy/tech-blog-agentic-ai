from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import logging
import json

from models import Article
from services.agentic_brain import generate_canonical_article

logger = logging.getLogger(__name__)

# =========================
# CONFIG
# =========================
WEAK_VIEW_THRESHOLD = 50
MAX_REWRITE_LIMIT = 2
GRACE_PERIOD_HOURS = 24


def is_ctr_weak(article: Article) -> bool:
    """
    Decide whether article is eligible for CTR optimization
    """

    if article.status != "published" or not article.published_at:
        return False

    age = datetime.utcnow() - article.published_at
    if age < timedelta(hours=GRACE_PERIOD_HOURS):
        return False

    if article.view_count is not None and article.view_count >= WEAK_VIEW_THRESHOLD:
        return False

    if article.rewrite_count is not None and article.rewrite_count >= MAX_REWRITE_LIMIT:
        return False

    return True


def generate_ctr_optimized_seo(article: Article) -> dict:
    """
    Generates improved SEO title & meta description
    using AI-based CTR optimization
    """

    prompt = f"""
You are an expert CTR optimization strategist.

TASK:
1. Identify TOP 3 important keywords from the content
2. Generate 3 SEO title variations
3. Internally select the BEST performing one

RULES:
- Title max 60 characters
- Meta description max 155 characters
- Professional & curiosity-driven
- No clickbait
- No emojis
- No markdown
- Output ONLY valid JSON

JSON FORMAT:
{{
  "seo_title": "...",
  "meta_description": "...",
  "keywords": "kw1,kw2,kw3"
}}

Article Title:
{article.title}

Article Content:
{article.canonical_content[:1500]}
"""

    try:
        raw = generate_canonical_article(
            master_prompt=prompt,
            user_topic=""
        )

        data = json.loads(raw)

        return {
            "seo_title": data.get("seo_title", article.seo_title),
            "meta_description": data.get(
                "meta_description",
                article.meta_description
            )
        }

    except Exception as e:
        logger.exception(
            f"SEO generation failed for article ID {article.id}: {e}"
        )
        return {
            "seo_title": article.seo_title,
            "meta_description": article.meta_description
        }


def optimize_article_ctr(db: Session, article_id: int) -> bool:
    """
    Full CTR optimization pipeline
    """

    try:
        article = db.query(Article).filter(Article.id == article_id).first()
        if not article:
            logger.warning(f"Article not found: ID {article_id}")
            return False

        if not is_ctr_weak(article):
            logger.info(f"CTR optimization skipped for article ID {article.id}")
            return False

        seo_data = generate_ctr_optimized_seo(article)

        article.seo_title = seo_data["seo_title"]
        article.meta_description = seo_data["meta_description"]
        article.rewrite_count = (article.rewrite_count or 0) + 1

        db.commit()

        logger.info(f"CTR optimized successfully for article ID {article.id}")
        return True

    except Exception as e:
        db.rollback()
        logger.exception(
            f"CTR optimization transaction failed for article ID {article_id}: {e}"
        )
        return False
