import json
from services.agentic_brain import generate_canonical_article


def generate_seo(article_title: str, article_content: str):
    """
    Generates SEO title, meta description and tags using AI.
    """

    seo_prompt = f"""
You are an expert SEO strategist.

Rules:
- Do NOT add extra text
- Output ONLY valid JSON

Format:
{{
  "seo_title": "...",
  "meta_description": "...",
  "seo_tags": "tag1,tag2,tag3"
}}

Article Title:
{article_title}

Article Content:
{article_content[:1200]}
"""

    raw_response = generate_canonical_article(
        master_prompt=seo_prompt,
        user_topic=""
    )

    try:
        data = json.loads(raw_response)
        return data
    except Exception:
        return {
            "seo_title": f"{article_title} – Complete Guide",
            "meta_description": article_title,
            "seo_tags": ""
        }
