from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from datetime import datetime
from backend.database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False, index=True)
    canonical_content = Column(Text, nullable=False)

    seo_title = Column(String(255), nullable=True, index=True)
    meta_description = Column(String(300), nullable=True)
    seo_tags = Column(String(300), nullable=True)

    platform_target = Column(String(50), nullable=False, index=True)
    status = Column(String(20), default="draft", index=True)

    auto_publish = Column(Boolean, default=True, index=True)
    language = Column(String(20), default="en")

    created_at = Column(DateTime, default=datetime.utcnow)
    published_at = Column(DateTime, nullable=True)

    view_count = Column(Integer, default=0)
    rewrite_count = Column(Integer, default=0)
    last_optimized_at = Column(DateTime, nullable=True)

    # 💰 REVENUE
    ads_enabled = Column(Boolean, default=True, index=True)

    # 🗑️ SOFT DELETE
    is_deleted = Column(Boolean, default=False, index=True)
    deleted_at = Column(DateTime, nullable=True)
