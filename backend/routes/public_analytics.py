from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from datetime import timedelta, date

from database import SessionLocal
from models import Article

router = APIRouter(
    prefix="/api/public/analytics",
    tags=["Public Analytics"]
)

# =========================
# DB
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# OVERVIEW
# =========================
@router.get("/overview")
def public_overview(db: Session = Depends(get_db)):
    total_articles = db.query(Article).filter(Article.is_deleted == False).count()

    published_articles = db.query(Article).filter(
        Article.status == "published",
        Article.is_deleted == False
    ).count()

    total_views = db.query(func.sum(Article.view_count)).scalar() or 0

    return {
        "total_articles": total_articles,
        "published_articles": published_articles,
        "total_views": total_views
    }

# =========================
# TRENDING
# =========================
@router.get("/trending")
def trending_articles(limit: int = 5, db: Session = Depends(get_db)):
    return (
        db.query(Article)
        .filter(
            Article.status == "published",
            Article.is_deleted == False
        )
        .order_by(Article.view_count.desc())
        .limit(limit)
        .all()
    )

# =========================
# DAILY VIEWS (LAST 30 DAYS)
# =========================
@router.get("/charts/daily")
def daily_views(db: Session = Depends(get_db)):
    today = date.today()
    start_date = today - timedelta(days=29)

    rows = (
        db.query(
            cast(Article.created_at, Date).label("day"),
            func.sum(Article.view_count).label("views")
        )
        .filter(
            Article.status == "published",
            Article.is_deleted == False,
            Article.created_at >= start_date
        )
        .group_by("day")
        .order_by("day")
        .all()
    )

    return [
        {"date": row.day, "views": int(row.views)}
        for row in rows
    ]

# =========================
# WEEKLY VIEWS (LAST 12 WEEKS)
# =========================
@router.get("/charts/weekly")
def weekly_views(db: Session = Depends(get_db)):
    rows = (
        db.query(
            func.strftime("%Y-%W", Article.created_at).label("week"),
            func.sum(Article.view_count).label("views")
        )
        .filter(
            Article.status == "published",
            Article.is_deleted == False
        )
        .group_by("week")
        .order_by("week")
        .limit(12)
        .all()
    )

    return [
        {"week": row.week, "views": int(row.views)}
        for row in rows
    ]

# =========================
# MONTHLY VIEWS (LAST 12 MONTHS)
# =========================
@router.get("/charts/monthly")
def monthly_views(db: Session = Depends(get_db)):
    rows = (
        db.query(
            func.strftime("%Y-%m", Article.created_at).label("month"),
            func.sum(Article.view_count).label("views")
        )
        .filter(
            Article.status == "published",
            Article.is_deleted == False
        )
        .group_by("month")
        .order_by("month")
        .limit(12)
        .all()
    )

    return [
        {"month": row.month, "views": int(row.views)}
        for row in rows
    ]
