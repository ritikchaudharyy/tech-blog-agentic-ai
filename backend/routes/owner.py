from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

# =========================
# LOCAL IMPORTS (DOCKER SAFE)
# =========================
from database import SessionLocal
from models import Article
from auth import verify_owner
from schemas import (
    ArticleListOut,
    ArticleUpdateRequest
)

from services.publishers.blogger import BloggerPublisher
from services.seo_generator import generate_seo
from services.blog_structure import generate_structured_blog
from services.html_builder import build_blog_html
from services.related_block import get_related_posts
from services.dashboard_service import (
    get_overview_stats,
    get_trending_memory_stats
)
from services.auto_scheduler import pick_best_article_to_publish

# =========================
# ROUTER
# =========================
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

# =========================
# DASHBOARD
# =========================
@router.get("/metrics")
def admin_metrics(db: Session = Depends(get_db)):
    return get_overview_stats(db)


@router.get("/traffic")
def admin_traffic(db: Session = Depends(get_db)):
    return get_trending_memory_stats(db)


@router.get("/articles", response_model=List[ArticleListOut])
def admin_articles(db: Session = Depends(get_db)):
    return (
        db.query(Article)
        .filter(Article.is_deleted == False)
        .order_by(Article.created_at.desc())
        .all()
    )

# =========================
# PHASE 4.4 — SOFT DELETE
# =========================
@router.delete("/articles/{article_id}")
def soft_delete_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    article.is_deleted = True
    article.deleted_at = datetime.utcnow()
    article.status = "deleted"

    db.commit()
    return {"message": "Article soft-deleted"}


@router.post("/articles/{article_id}/restore")
def restore_article(article_id: int, db: Session = Depends(get_db)):
    article = (
        db.query(Article)
        .filter(Article.id == article_id, Article.is_deleted == True)
        .first()
    )
    if not article:
        raise HTTPException(status_code=404, detail="Deleted article not found")

    article.is_deleted = False
    article.deleted_at = None
    article.status = "approved"

    db.commit()
    return {"message": "Article restored successfully"}

# =========================
# PHASE 5 — ANALYTICS
# =========================
@router.get("/articles/{article_id}/analytics")
def article_analytics(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    return {
        "article_id": article.id,
        "title": article.title,
        "view_count": article.view_count,
        "rewrite_count": article.rewrite_count,
        "status": article.status,
        "created_at": article.created_at,
        "published_at": article.published_at
    }

# =========================
# PHASE 6 — ADS CONTROL
# =========================
@router.post("/articles/{article_id}/ads/enable")
def enable_ads(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    article.ads_enabled = True
    db.commit()
    return {"message": "Ads enabled"}


@router.post("/articles/{article_id}/ads/disable")
def disable_ads(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    article.ads_enabled = False
    db.commit()
    return {"message": "Ads disabled"}

# =========================
# PHASE 7 — AI AUTO SCHEDULER
# =========================
@router.post("/auto-scheduler/run")
def run_auto_scheduler(db: Session = Depends(get_db)):
    article = pick_best_article_to_publish(db)

    if not article:
        return {"message": "No article ready for auto-publish"}

    if article.is_deleted or article.status == "published":
        return {"message": "Article not eligible for publishing"}

    publisher = BloggerPublisher()
    result = publisher.publish(article)

    article.status = "published"
    article.published_at = datetime.utcnow()
    db.commit()

    return {
        "message": "Auto-scheduler published article",
        "article_id": article.id,
        "url": result.get("url")
    }

# =========================
# MANUAL PUBLISH
# =========================
@router.post("/articles/{article_id}/publish")
def publish_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()

    if not article or article.is_deleted:
        raise HTTPException(status_code=404, detail="Article not publishable")

    if article.status == "published":
        return {"message": "Article already published"}

    publisher = BloggerPublisher()
    result = publisher.publish(article)

    article.status = "published"
    article.published_at = datetime.utcnow()
    db.commit()

    return {"message": "Published successfully", "url": result.get("url")}

# =========================
# PHASE 4.3 — EDIT
# =========================
@router.put("/articles/{article_id}")
def update_article(
    article_id: int,
    payload: ArticleUpdateRequest,
    db: Session = Depends(get_db)
):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article or article.is_deleted:
        raise HTTPException(status_code=404, detail="Article not editable")

    if payload.title:
        article.title = payload.title

    if payload.canonical_content:
        article.canonical_content = payload.canonical_content

    article.status = "approved"
    article.rewrite_count += 1
    article.last_optimized_at = datetime.utcnow()

    db.commit()
    return {"message": "Article updated successfully"}

# =========================
# PHASE 4.3 — RE-OPTIMIZE
# =========================
@router.post("/articles/{article_id}/re-optimize")
def re_optimize_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article or article.is_deleted:
        raise HTTPException(status_code=404, detail="Article not optimizable")

    structure = generate_structured_blog(article.title)
    related_posts = get_related_posts(db)

    new_html = build_blog_html(
        structure=structure,
        title=article.title,
        related_posts=related_posts
    )

    seo = generate_seo(article.title, new_html)

    article.canonical_content = new_html
    article.seo_title = seo.get("seo_title")
    article.meta_description = seo.get("meta_description")
    article.seo_tags = seo.get("seo_tags")

    article.status = "approved"
    article.rewrite_count += 1
    article.last_optimized_at = datetime.utcnow()

    db.commit()
    return {"message": "Article re-optimized successfully"}
