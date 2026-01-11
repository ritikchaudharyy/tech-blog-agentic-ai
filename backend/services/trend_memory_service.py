from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models_trend_memory import TrendMemory

COOLDOWN_DAYS = 14
MAX_USAGE = 3


def record_trend_usage(db: Session, topic: str):
    record = (
        db.query(TrendMemory)
        .filter(TrendMemory.topic == topic)
        .first()
    )

    if record:
        record.times_used += 1
        record.last_used_at = datetime.utcnow()
    else:
        record = TrendMemory(
            topic=topic
        )
        db.add(record)

    db.commit()


def is_topic_allowed(db: Session, topic: str) -> bool:
    record = (
        db.query(TrendMemory)
        .filter(TrendMemory.topic == topic)
        .first()
    )

    if not record:
        return True

    if record.times_used >= MAX_USAGE:
        return False

    if datetime.utcnow() - record.last_used_at < timedelta(days=COOLDOWN_DAYS):
        return False

    return True
