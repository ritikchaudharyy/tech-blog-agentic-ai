def inject_images(html: str, topic: str) -> str:
    hero = f"""
    <figure>
        <img src="https://source.unsplash.com/1200x600/?{topic.replace(' ', ',')}"
             alt="{topic}" />
        <figcaption>{topic}</figcaption>
    </figure>
    """

    return hero + html
