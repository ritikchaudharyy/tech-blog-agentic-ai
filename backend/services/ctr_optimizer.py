from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from backend.models import Article
from backend.services.agentic_brain import generate_canonical_article


WEAK_VIEW_THRESHOLD = 50
MAX_REWRITE_LIMIT = 2
GRACE_PERIOD_HOURS = 24


def is_ctr_weak(article: Article) -> bool:
    """
    Decide if article needs CTR optimization
    """

    # 1. Grace period check (very important)
    if not article.published_at:
        return False

    if datetime.utcnow() - article.published_at < timedelta(hours=GRACE_PERIOD_HOURS):
        return False

    # 2. Enough views? Then skip
    if article.view_count >= WEAK_VIEW_THRESHOLD:
        return False

    # 3. Rewrite limit reached?
    if article.rewrite_count >= MAX_REWRITE_LIMIT:
        return False

    return True


def generate_ctr_optimized_seo(article: Article) -> dict:
    """
    Generate better SEO title & meta description using AI
    """

    prompt = f"""
You are a senior SEO strategist.

TASK:
Improve click-through rate for the following article.

STRICT RULES:
- Output ONLY valid JSON
- No explanations
- No markdown
- No emojis
- Professional tone (no clickbait)

PROCESS:
1. Extract top 3 SEO keywords from the content
2. Generate 3 SEO title variations (max 60 chars)
3. Pick the BEST title (curiosity-driven, professional)
4. Generate meta description (max 155 chars)

JSON FORMAT:
{{
  "seo_title": "...",
  "meta_description": "...",
  "keywords": ["keyword1", "keyword2", "keyword3"]
}}

Article Title:
{article.title}

Article Content:
{article.canonical_content[:1500]}
"""

    raw = generate_canonical_article(
        master_prompt="",
        user_topic=prompt
    )

    try:
        import json
        data = json.loads(raw)
        return {
            "seo_title": data.get("seo_title", article.seo_title),
            "meta_description": data.get("meta_description", article.meta_description)
        }
    except Exception:
        # Safe fallback (never crash)
        return {
            "seo_title": article.seo_title,
            "meta_description": article.meta_description
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
