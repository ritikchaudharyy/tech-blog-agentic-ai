from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    excerpt = Column(String(500))
    author = Column(String(100), default="AI Agent")
    status = Column(String(50), default="Published")
    views = Column(Integer, default=0)
    published_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)