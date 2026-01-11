from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base


class TrendMemory(Base):
    __tablename__ = "trend_memory"

    id = Column(Integer, primary_key=True, index=True)

    topic = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    times_used = Column(
        Integer,
        default=1
    )

    last_used_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
