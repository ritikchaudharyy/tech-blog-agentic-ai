from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from backend.database import SessionLocal
from backend.models import Article
from backend.auth import verify_owner
from backend.schemas import GenerateDraftRequest, ArticleListOut

from backend.services.publishers.blogger import BloggerPublisher
from backend.services.seo_generator import generate_seo
from backend.services.blog_structure import generate_structured_blog
from backend.services.html_builder import build_blog_html
from backend.services.related_block import get_related_posts
from backend.services.memory_trending_picker import pick_memory_safe_trending_topic
from backend.services.trend_memory_service import record_trend_usage
from backend.services.dashboard_service import (
    get_overview_stats,
    get_low_view_articles,
    get_top_articles,
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
# ADMIN DASHBOARD APIs (FRONTEND REQUIRED)
# =====================================================

@router.get("/metrics")
def admin_metrics(db: Session = Depends(get_db)):
    """
    Used by AdminDashboard.jsx
    """
    return get_overview_stats(db)


@router.get("/traffic")
def admin_traffic(db: Session = Depends(get_db)):
    """
    Used by AdminDashboard.jsx (charts)
    """
    return get_trending_memory_stats(db)


@router.get("/articles", response_model=List[ArticleListOut])
def admin_articles(db: Session = Depends(get_db)):
    """
    Used by AdminContent.jsx
    """
    return db.query(Article).all()

# =====================================================
# AUTO PUBLISH (MANUAL)
# =====================================================

@router.post("/auto-publish")
def auto_publish(payload: GenerateDraftRequest, db: Session = Depends(get_db)):

    structure = generate_structured_blog(payload.topic)
    related_posts = get_related_posts(db)

    html_content = build_blog_html(
        structure=structure,
        title=payload.topic,
        related_posts=related_posts
    )

    seo = generate_seo(
        article_title=payload.topic,
        article_content=html_content
    )

    article = Article(
        title=payload.topic,
        canonical_content=html_content,
        seo_title=seo.get("seo_title"),
        meta_description=seo.get("meta_description"),
        seo_tags=seo.get("seo_tags"),
        platform_target=payload.platform,
        status="approved",
        auto_publish=True
    )

    db.add(article)
    db.commit()
    db.refresh(article)

    publisher = BloggerPublisher()
    result = publisher.publish(article)

    article.status = "published"
    db.commit()

    record_trend_usage(db, payload.topic)

    return {
        "message": "Article published successfully",
        "url": result.get("url")
    }

# =====================================================
# AUTO PUBLISH (TRENDING)
# =====================================================

@router.post("/auto-publish/trending")
def auto_publish_trending(region: str = "global", db: Session = Depends(get_db)):

    topic = pick_memory_safe_trending_topic(db, region)
    structure = generate_structured_blog(topic)
    related_posts = get_related_posts(db)

    html_content = build_blog_html(
        structure=structure,
        title=topic,
        related_posts=related_posts
    )

    seo = generate_seo(
        article_title=topic,
        article_content=html_content
    )

    article = Article(
        title=topic,
        canonical_content=html_content,
        seo_title=seo.get("seo_title"),
        meta_description=seo.get("meta_description"),
        seo_tags=seo.get("seo_tags"),
        platform_target="blogger",
        status="approved",
        auto_publish=True
    )

    db.add(article)
    db.commit()
    db.refresh(article)

    publisher = BloggerPublisher()
    result = publisher.publish(article)

    article.status = "published"
    db.commit()

    record_trend_usage(db, topic)

    return {
        "message": "Trending article auto-published",
        "topic": topic,
        "url": result.get("url")
    }

# =====================================================
# PAUSE / RESUME AUTO PUBLISH
# =====================================================

@router.post("/auto-publish/pause")
def pause_auto_publish(db: Session = Depends(get_db)):
    db.query(Article).update({"auto_publish": False})
    db.commit()
    return {"message": "Auto publishing paused"}


@router.post("/auto-publish/resume")
def resume_auto_publish(db: Session = Depends(get_db)):
    db.query(Article).update({"auto_publish": True})
    db.commit()
    return {"message": "Auto publishing resumed"}
