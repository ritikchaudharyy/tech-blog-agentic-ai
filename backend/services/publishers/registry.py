from services.publishers.blogger import BloggerPublisher
from services.publishers.wordpress import WordPressPublisher


def get_publisher(platform: str):
    platform = platform.lower()

    if platform == "blogger":
        return BloggerPublisher()

    if platform == "wordpress":
        return WordPressPublisher()

    raise ValueError("Unsupported publishing platform")
