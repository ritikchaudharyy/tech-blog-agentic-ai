import json
from services.agentic_brain import call_llm  # same LLM used earlier
from services.seo_prompt import build_seo_prompt


def generate_seo_metadata(title: str, content: str):
    prompt = build_seo_prompt(title, content)

    raw_output = call_llm(prompt)

    try:
        seo_data = json.loads(raw_output)
    except Exception:
        raise ValueError("Invalid SEO JSON generated")

    return {
        "seo_title": seo_data.get("seo_title"),
        "meta_description": seo_data.get("meta_description"),
        "seo_tags": seo_data.get("seo_tags"),
    }
