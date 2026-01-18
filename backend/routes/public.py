from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
from models import Article
from schemas import ArticleListOut, ArticleDetailOut

router = APIRouter(
    prefix="/api/articles",
    tags=["Public Articles"]
)

# =========================
# DB DEPENDENCY
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# GET TRENDING ARTICLES
# =========================
@router.get("/trending", response_model=List[ArticleListOut])
def get_trending_articles(db: Session = Depends(get_db)):
    articles = (
        db.query(Article)
        .filter(Article.status == "published")
        .order_by(Article.views.desc())
        .limit(6)
        .all()
    )
    return articles

# =========================
# GET ALL ARTICLES
# =========================
@router.get("/", response_model=List[ArticleListOut])
def get_all_articles(db: Session = Depends(get_db)):
    articles = (
        db.query(Article)
        .filter(Article.status == "published")
        .all()
    )
    return articles

# =========================
# GET ARTICLE BY ID
# =========================
@router.get("/{article_id}", response_model=ArticleDetailOut)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = (
        db.query(Article)
        .filter(
            Article.id == article_id,
            Article.status == "published"
        )
        .first()
    )

    if not article:
        raise HTTPException(
            status_code=404,
            detail="Article not found"
        )

    return article

# =========================
# SEARCH ARTICLES
# =========================
@router.get("/search/{keyword}", response_model=List[ArticleListOut])
def search_articles(keyword: str, db: Session = Depends(get_db)):
    results = (
        db.query(Article)
        .filter(
            Article.title.ilike(f"%{keyword}%"),
            Article.status == "published"
        )
        .all()
    )
    return results
