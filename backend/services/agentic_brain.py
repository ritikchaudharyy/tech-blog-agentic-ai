import os
import logging
from dotenv import load_dotenv
from google import genai

# =========================
# ENV & LOGGING
# =========================
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing in environment variables")

# =========================
# GENAI CLIENT
# =========================
client = genai.Client(api_key=GEMINI_API_KEY)


def generate_canonical_article(master_prompt: str, user_topic: str) -> str:
    """
    Generates a canonical article in plain text.
    No HTML. No markdown. No SEO metadata.
    """

    prompt = f"""
{master_prompt}

User Input:
{user_topic}

IMPORTANT RULES:
- Generate ONLY the canonical article
- Plain text only
- No HTML, markdown, bullets, or headings
- Professional, human-written tech blog
"""

    try:
        response = client.models.generate_content(
            model="models/gemini-flash-lite-latest",
            contents=prompt
        )

        if not response or not response.text:
            logger.error("Empty response received from Gemini")
            return ""

        return response.text.strip()

    except Exception:
        logger.exception("Gemini content generation failed")
        return ""
