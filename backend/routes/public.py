from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models import Article

router = APIRouter(prefix="/articles", tags=["Public Articles"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_all_articles(db: Session = Depends(get_db)):
    articles = db.query(Article).filter(Article.status == "published").all()
    return articles


@router.get("/{article_id}")
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(
        Article.id == article_id,
        Article.status == "published"
    ).first()
    return article


@router.get("/search/{keyword}")
def search_articles(keyword: str, db: Session = Depends(get_db)):
    results = db.query(Article).filter(
        Article.title.contains(keyword),
        Article.status == "published"
    ).all()
    return results
