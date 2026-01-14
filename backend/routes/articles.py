from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import Article

router = APIRouter(prefix="/api/articles", tags=["Articles"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{article_id}")
def read_article(article_id: int, db: Session = Depends(get_db)):
    article = (
        db.query(Article)
        .filter(Article.id == article_id, Article.is_deleted == False)
        .first()
    )

    if not article or article.status != "published":
        raise HTTPException(status_code=404, detail="Article not found")

    # 🔥 Atomic view increment
    article.view_count += 1
    db.commit()

    return article
