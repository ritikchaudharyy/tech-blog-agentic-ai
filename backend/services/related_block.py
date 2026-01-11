from sqlalchemy.orm import Session
from models import Article
import re


def get_related_posts(db: Session, limit: int = 5):
    """
    Fetch latest published articles
    (STEP 17.2.1)
    """
    return (
        db.query(Article)
        .filter(Article.status == "published")
        .order_by(Article.created_at.desc())
        .limit(limit)
        .all()
    )


def _slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text.strip())
    return text


def build_related_posts_html(posts) -> str:
    """
    STEP 17.2.2 — HTML Builder
    """
    if not posts:
        return ""

    html = """
    <hr/>
    <h2 style="margin-top:40px;">Related Articles</h2>
    <ul style="line-height:1.8; padding-left:18px;">
    """

    for post in posts:
        slug = _slugify(post.title)
        html += f"""
        <li>
            <a href="/{slug}" style="text-decoration:none;">
                {post.title}
            </a>
        </li>
        """

    html += "</ul>"
    return html
