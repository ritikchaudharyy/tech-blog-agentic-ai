from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from backend.models import Article
from backend.services.agentic_brain import generate_canonical_article

# =========================
# CONFIG
# =========================
WEAK_VIEW_THRESHOLD = 50          # proxy CTR signal
MAX_REWRITE_LIMIT = 2
GRACE_PERIOD_HOURS = 24


def is_ctr_weak(article: Article) -> bool:
    """
    Decide whether article is eligible for CTR optimization
    """

    # 1️⃣ Must be published
    if article.status != "published" or not article.published_at:
        return False

    # 2️⃣ Grace period check
    age = datetime.utcnow() - article.published_at
    if age < timedelta(hours=GRACE_PERIOD_HOURS):
        return False

    # 3️⃣ View threshold
    if article.view_count >= WEAK_VIEW_THRESHOLD:
        return False

    # 4️⃣ Rewrite limit
    if article.rewrite_count >= MAX_REWRITE_LIMIT:
        return False

    return True


def generate_ctr_optimized_seo(article: Article) -> dict:
    """
    Generates improved SEO title & meta description
    using smarter CTR prompt
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

    raw = generate_canonical_article(
        master_prompt=prompt,
        user_topic=""
    )

    try:
        import json
        data = json.loads(raw)

        return {
            "seo_title": data.get("seo_title", article.seo_title),
            "meta_description": data.get(
                "meta_description",
                article.meta_description
            )
        }

    except Exception:
        # fallback safety
        return {
            "seo_title": article.seo_title,
            "meta_description": article.meta_description
        }


def optimize_article_ctr(db: Session, article_id: int) -> bool:
    """
    Full CTR optimization pipeline
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
