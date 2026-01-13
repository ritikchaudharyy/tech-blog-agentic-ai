from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from backend.database import SessionLocal
from backend.models import Article
from backend.auth import verify_owner
from backend.schemas import (
    GenerateDraftRequest,
    ArticleListOut,
    ArticleUpdateRequest
)

from backend.services.publishers.blogger import BloggerPublisher
from backend.services.seo_generator import generate_seo
from backend.services.blog_structure import generate_structured_blog
from backend.services.html_builder import build_blog_html
from backend.services.related_block import get_related_posts
from backend.services.memory_trending_picker import pick_memory_safe_trending_topic
from backend.services.trend_memory_service import record_trend_usage
from backend.services.dashboard_service import (
    get_overview_stats,
    get_trending_memory_stats
)

router = APIRouter(
    prefix="/api/admin",
    tags=["Admin Control"],
    dependencies=[Depends(verify_owner)]
)

# =========================
# DATABASE DEPENDENCY
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =====================================================
# DASHBOARD
# =====================================================

@router.get("/metrics")
def admin_metrics(db: Session = Depends(get_db)):
    return get_overview_stats(db)


@router.get("/traffic")
def admin_traffic(db: Session = Depends(get_db)):
    return get_trending_memory_stats(db)


@router.get("/articles", response_model=List[ArticleListOut])
def admin_articles(db: Session = Depends(get_db)):
    return db.query(Article).order_by(Article.created_at.desc()).all()

# =====================================================
# PHASE 4.2 — PUBLISH / DELETE
# =====================================================

@router.post("/articles/{article_id}/publish")
def publish_article(article_id: int, db: Session = Depends(get_db)):

    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    publisher = BloggerPublisher()
    result = publisher.publish(article)

    article.status = "published"
    article.published_at = datetime.utcnow()

    db.commit()

    return {
        "message": "Article published",
        "url": result.get("url")
    }


@router.delete("/articles/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db)):

    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    db.delete(article)
    db.commit()

    return {"message": "Article deleted"}

# =====================================================
# PHASE 4.3 — EDIT ARTICLE
# =====================================================

@router.put("/articles/{article_id}")
def update_article(
    article_id: int,
    payload: ArticleUpdateRequest,
    db: Session = Depends(get_db)
):
    """
    Admin manual edit
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    if payload.title:
        article.title = payload.title

    if payload.canonical_content:
        article.canonical_content = payload.canonical_content

    article.status = "approved"
    article.rewrite_count += 1
    article.last_optimized_at = datetime.utcnow()

    db.commit()
    db.refresh(article)

    return {
        "message": "Article updated",
        "rewrite_count": article.rewrite_count
    }

# =====================================================
# PHASE 4.3 — RE-OPTIMIZE (AI + SEO)
# =====================================================

@router.post("/articles/{article_id}/re-optimize")
def re_optimize_article(article_id: int, db: Session = Depends(get_db)):
    """
    Full AI re-optimization:
    - Structure
    - SEO
    - HTML
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    structure = generate_structured_blog(article.title)
    related_posts = get_related_posts(db)

    new_html = build_blog_html(
        structure=structure,
        title=article.title,
        related_posts=related_posts
    )

    seo = generate_seo(
        article_title=article.title,
        article_content=new_html
    )

    article.canonical_content = new_html
    article.seo_title = seo.get("seo_title")
    article.meta_description = seo.get("meta_description")
    article.seo_tags = seo.get("seo_tags")

    article.status = "approved"
    article.rewrite_count += 1
    article.last_optimized_at = datetime.utcnow()

    db.commit()
    db.refresh(article)

    return {
        "message": "Article re-optimized successfully",
        "rewrite_count": article.rewrite_count
    }
