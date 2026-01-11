from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Article
from auth import verify_owner
from schemas import GenerateDraftRequest

from services.publishers.blogger import BloggerPublisher
from services.seo_generator import generate_seo
from services.blog_structure import generate_structured_blog
from services.html_builder import build_blog_html
from services.related_block import get_related_posts
from services.memory_trending_picker import pick_memory_safe_trending_topic
from services.trend_memory_service import record_trend_usage
from services.dashboard_service import (
    get_overview_stats,
    get_low_view_articles,
    get_top_articles,
    get_trending_memory_stats
)

router = APIRouter(
    prefix="/owner",
    tags=["Owner Control"],
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
# AUTO PUBLISH (MANUAL)
# =========================

@router.post("/auto-publish")
def auto_publish(payload: GenerateDraftRequest, db: Session = Depends(get_db)):

    # 1. Generate structured blog content
    structure = generate_structured_blog(payload.topic)

    # 2. Fetch related posts for internal linking
    related_posts = get_related_posts(db)

    # 3. Build Blogger-safe HTML (TITLE IS REQUIRED)
    html_content = build_blog_html(
        structure=structure,
        title=payload.topic,
        related_posts=related_posts
    )

    # 4. Generate SEO metadata
    seo = generate_seo(
        article_title=payload.topic,
        article_content=html_content
    )

    # 5. Save article to database
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

    # 6. Publish to Blogger
    publisher = BloggerPublisher()
    result = publisher.publish(article)

    # 7. Update status
    article.status = "published"
    db.commit()

    # 8. Record topic usage (memory-safe)
    record_trend_usage(db, payload.topic)

    return {
        "message": "Article published successfully",
        "url": result.get("url")
    }

# =========================
# AUTO PUBLISH (TRENDING)
# =========================

@router.post("/auto-publish/trending")
def auto_publish_trending(region: str = "global", db: Session = Depends(get_db)):

    # 1. Pick a memory-safe trending topic
    topic = pick_memory_safe_trending_topic(db, region)

    # 2. Generate structured blog content
    structure = generate_structured_blog(topic)

    # 3. Fetch related posts
    related_posts = get_related_posts(db)

    # 4. Build Blogger-safe HTML (TITLE IS REQUIRED)
    html_content = build_blog_html(
        structure=structure,
        title=topic,
        related_posts=related_posts
    )

    # 5. Generate SEO metadata
    seo = generate_seo(
        article_title=topic,
        article_content=html_content
    )

    # 6. Save article to database
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

    # 7. Publish to Blogger
    publisher = BloggerPublisher()
    result = publisher.publish(article)

    # 8. Update status
    article.status = "published"
    db.commit()

    # 9. Record topic usage
    record_trend_usage(db, topic)

    return {
        "message": "Trending article auto-published",
        "topic": topic,
        "url": result.get("url")
    }

# =========================
# DASHBOARD INSIGHTS
# =========================

@router.get("/dashboard/overview")
def dashboard_overview(db: Session = Depends(get_db)):
    return get_overview_stats(db)

@router.get("/dashboard/low-view")
def dashboard_low_view(db: Session = Depends(get_db)):
    return get_low_view_articles(db)

@router.get("/dashboard/top-articles")
def dashboard_top_articles(db: Session = Depends(get_db)):
    return get_top_articles(db)

@router.get("/dashboard/trending-memory")
def dashboard_trending_memory(db: Session = Depends(get_db)):
    return get_trending_memory_stats(db)

# =========================
# PAUSE / RESUME AUTO PUBLISH
# =========================

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
