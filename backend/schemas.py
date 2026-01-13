from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# =========================
# DRAFT / GENERATION
# =========================
class GenerateDraftRequest(BaseModel):
    topic: str
    platform: str = "blogger"


# =========================
# ADMIN UPDATE (PHASE 4.3)
# =========================
class ArticleUpdateRequest(BaseModel):
    """
    Used for manual admin edits
    """
    title: Optional[str] = None
    canonical_content: Optional[str] = None


# =========================
# ARTICLE RESPONSE SCHEMAS
# =========================

class ArticleBase(BaseModel):
    id: int
    title: str

    # Mapped from meta_description for frontend compatibility
    summary: Optional[str] = Field(None, alias="meta_description")

    # Core DB fields
    view_count: int
    status: str
    created_at: datetime
    platform_target: str

    # Admin / UI derived
    verified: bool = False

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ArticleListOut(ArticleBase):
    """
    Used for:
    - Admin content table
    - Trending articles
    - Search results
    """
    pass


class ArticleDetailOut(ArticleBase):
    """
    Used for:
    - Single article page
    - Admin preview
    """

    # Mapped from canonical_content
    content: Optional[str] = Field(None, alias="canonical_content")

    # SEO (optional but future-safe)
    seo_title: Optional[str] = None
    meta_description: Optional[str] = None
    seo_tags: Optional[str] = None

    # Intelligence
    rewrite_count: Optional[int] = 0
    last_optimized_at: Optional[datetime] = None
