from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date


# =========================
# DRAFT / GENERATION
# =========================
class GenerateDraftRequest(BaseModel):
    topic: str
    platform: str = "blogger"


# =========================
# ADMIN UPDATE
# =========================
class ArticleUpdateRequest(BaseModel):
    title: Optional[str] = None
    canonical_content: Optional[str] = None


# =========================
# PUBLIC ANALYTICS (CHARTS)
# =========================
class TimeSeriesPoint(BaseModel):
    date: date
    views: int


class PublicOverviewStats(BaseModel):
    total_articles: int
    published_articles: int
    total_views: int


# =========================
# ARTICLE RESPONSE
# =========================
class ArticleBase(BaseModel):
    id: int
    title: str
    summary: Optional[str] = Field(None, alias="meta_description")

    view_count: int
    status: str
    created_at: datetime
    platform_target: str

    is_deleted: bool = False
    deleted_at: Optional[datetime] = None

    verified: bool = False

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ArticleListOut(ArticleBase):
    pass


class ArticleDetailOut(ArticleBase):
    content: Optional[str] = Field(None, alias="canonical_content")

    seo_title: Optional[str] = None
    meta_description: Optional[str] = None
    seo_tags: Optional[str] = None

    rewrite_count: Optional[int] = 0
    last_optimized_at: Optional[datetime] = None
