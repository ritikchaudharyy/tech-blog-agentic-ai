from sqlalchemy.orm import Session
from services.trending_agent import get_trending_topics
from services.prompt_loader import load_master_prompt
from services.trend_memory_service import is_topic_allowed


def pick_memory_safe_trending_topic(
    db: Session,
    region: str = "global"
):
    master_prompt = load_master_prompt()

    topics = get_trending_topics(
        master_prompt=master_prompt,
        region=region,
        limit=5
    )

    for topic in topics:
        if is_topic_allowed(db, topic):
            return topic

    raise Exception("No memory-safe trending topic available")
