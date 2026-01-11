from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from datetime import datetime
from database import Base


class Article(Base):
    __tablename__ = "articles"

    # =========================
    # PRIMARY KEY
    # =========================
    id = Column(Integer, primary_key=True, index=True)

    # =========================
    # CORE CONTENT
    # =========================
    title = Column(
        String(255),
        nullable=False,
        index=True
    )

    canonical_content = Column(
        Text,
        nullable=False
    )

    # =========================
    # SEO SUPER ENGINE (STEP 14–15)
    # =========================
    seo_title = Column(
        String(255),
        nullable=True,
        index=True
    )

    meta_description = Column(
        String(300),
        nullable=True
    )

    seo_tags = Column(
        String(300),
        nullable=True
    )

    # =========================
    # PLATFORM & STATUS CONTROL
    # =========================
    platform_target = Column(
        String(50),
        nullable=False,
        index=True
    )

    status = Column(
        String(20),
        default="draft",
        index=True
    )

    # =========================
    # AUTOMATION CONTROL
    # =========================
    auto_publish = Column(
        Boolean,
        default=True,
        index=True
    )

    # =========================
    # LANGUAGE & TIMESTAMPS
    # =========================
    language = Column(
        String(20),
        default="en"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    published_at = Column(
        DateTime,
        nullable=True
    )

    # =========================
    # ANALYTICS & INTELLIGENCE (STEP 18.1)
    # =========================
    view_count = Column(
        Integer,
        default=0
    )

    rewrite_count = Column(
        Integer,
        default=0
    )

    last_optimized_at = Column(
        DateTime,
        nullable=True
    )

    # =========================
    # REPRESENTATION
    # =========================
    def __repr__(self):
        return (
            f"<Article(id={self.id}, "
            f"title='{self.title}', "
            f"status='{self.status}', "
            f"platform='{self.platform_target}', "
            f"views={self.view_count})>"
        )
        