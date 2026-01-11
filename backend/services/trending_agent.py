from backend.services.agentic_brain import generate_canonical_article


def get_trending_topics(
    master_prompt: str,
    region: str = "global",
    limit: int = 5
):
    """
    Returns a list of trending tech topics (titles only).
    No articles, no HTML, no publishing.
    """

    prompt = f"""
{master_prompt}

TASK:
Suggest {limit} trending TECHNOLOGY blog topics.

RULES:
- Topics must be recent and relevant
- Focus on AI, software, gadgets, startups, future tech
- Region focus: {region}
- Output ONLY topic titles
- One topic per line
- No explanations
- No numbering
"""

    response = generate_canonical_article(
        master_prompt="",
        user_topic=prompt
    )

    topics = [
        line.strip()
        for line in response.split("\n")
        if line.strip()
    ]

    return topics
