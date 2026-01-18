from sqlalchemy.orm import Session
from models import Article


def generate_weekly_newsletter(db: Session):
    articles = (
        db.query(Article)
        .filter(
            Article.status == "published",
            Article.is_deleted == False
        )
        .order_by(Article.view_count.desc())
        .limit(5)
        .all()
    )

    content = "🔥 Weekly Top Articles\n\n"

    for idx, article in enumerate(articles, start=1):
        content += f"{idx}. {article.title}\n"

    return {
        "subject": "Your Weekly Tech Digest 🚀",
        "content": content
    }
