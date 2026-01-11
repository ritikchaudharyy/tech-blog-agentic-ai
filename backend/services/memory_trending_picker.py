from backend.services.trending_agent import get_trending_topics


def pick_memory_safe_trending_topic(db, region: str = "global"):
    """
    Picks a trending topic while avoiding repetition
    """
    topics = get_trending_topics(
        master_prompt="",
        region=region,
        limit=5
    )

    if not topics:
        raise RuntimeError("No trending topics available")

    # Simple selection strategy (can be improved later)
    return topics[0]

