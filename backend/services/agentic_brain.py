import os
import logging
from dotenv import load_dotenv
import google.generativeai as genai

# =========================
# ENV & LOGGING
# =========================
# Do NOT override Docker environment variables
load_dotenv(override=False)

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# =========================
# GENAI SETUP (LAZY)
# =========================
_model = None


def get_gemini_model():
    """
    Lazily initializes and returns the Gemini model.
    This prevents app crash on startup if API key is missing.
    """
    global _model

    if _model is not None:
        return _model

    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY is missing. AI generation disabled.")
        return None

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        _model = genai.GenerativeModel("gemini-1.5-flash")
        logger.info("Gemini model initialized successfully")
        return _model

    except Exception as e:
        logger.exception(f"Failed to initialize Gemini model: {e}")
        return None


def generate_canonical_article(master_prompt: str, user_topic: str) -> str:
    """
    Generates canonical article content using Gemini.
    Returns plain text only.
    NEVER raises exception (safe for schedulers).
    """

    model = get_gemini_model()
    if model is None:
        logger.warning("Gemini model unavailable. Skipping content generation.")
        return ""

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
        response = model.generate_content(prompt)

        if not response or not getattr(response, "text", None):
            logger.error("Empty response received from Gemini")
            return ""

        return response.text.strip()

    except Exception as e:
        logger.exception(f"Gemini content generation failed: {e}")
        return ""
