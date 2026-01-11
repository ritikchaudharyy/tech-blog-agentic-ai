import json
from backend.services.agentic_brain import generate_canonical_article


BLOG_STRUCTURE_PROMPT = """
You are a professional senior tech blog editor.

STRICT RULES:
- Output ONLY valid JSON
- Do NOT add explanations, comments, markdown, or extra text
- Do NOT repeat the blog title as a heading
- Headings must be meaningful, SEO-friendly, and professional
- Content must be written in simple, clear English
- Paragraphs must be well structured (not one-liners)

CONTENT RULES:
- summary_hook: 2–3 short italic-style introductory lines
- sections: 4–6 main sections minimum
- Each section must have either:
  - direct "content", OR
  - "subsections" (2–4 per section)
- conclusion must be a strong closing paragraph

JSON FORMAT (STRICT):
{
  "summary_hook": "Intro text",
  "sections": [
    {
      "heading": "Main section heading",
      "content": "Detailed paragraph content"
    },
    {
      "heading": "Main section heading",
      "subsections": [
        {
          "subheading": "Sub heading",
          "content": "Detailed paragraph content"
        }
      ]
    }
  ],
  "conclusion": "Final closing paragraph"
}
"""


def generate_structured_blog(title: str) -> dict:
    """
    Generates a structured blog layout (JSON)
    used by HTML builder for professional blog rendering.
    """

    raw = generate_canonical_article(
        master_prompt=BLOG_STRUCTURE_PROMPT,
        user_topic=title
    )

    try:
        data = json.loads(raw)

        # Basic validation
        if not data.get("sections"):
            raise ValueError("No sections generated")

        if not data.get("summary_hook"):
            raise ValueError("Missing summary_hook")

        if not data.get("conclusion"):
            raise ValueError("Missing conclusion")

        return data

    except Exception as e:
        raise ValueError(
            f"AI did not return valid structured JSON: {str(e)}"
        )
