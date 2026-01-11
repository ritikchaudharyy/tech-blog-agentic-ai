def build_seo_prompt(article_title: str, article_content: str):
    return f"""
You are an expert SEO strategist and content editor.

Based on the article below, generate STRICTLY:

1. SEO Title (max 60 characters, compelling, Google friendly)
2. Meta Description (150–160 characters, click-worthy)
3. SEO Tags (5–8 comma-separated keywords)

Rules:
- Do NOT explain anything
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
{article_content[:1500]}
"""