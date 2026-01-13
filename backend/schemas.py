from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# =========================
# EXISTING SCHEMA
# =========================
class GenerateDraftRequest(BaseModel):
    topic: str
    platform: str = "blogger"


# =========================
# ARTICLE RESPONSE SCHEMAS
# =========================

class ArticleBase(BaseModel):
    id: int
    title: str
    # Mapped from meta_description for frontend compatibility
    summary: Optional[str] = Field(None, alias="meta_description")
    
    # DB fields
    view_count: int
    status: str
    created_at: datetime
    platform_target: str
    
    # Computed or default for now (since not in DB)
    verified: bool = False

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ArticleListOut(ArticleBase):
    """
    Used for:
    - Trending articles
    - Article listings
    - Search results
    """
    pass


class ArticleDetailOut(ArticleBase):
    """
    Used for:
    - Single article page
    """
    # Mapped from canonical_content
    content: Optional[str] = Field(None, alias="canonical_content")

