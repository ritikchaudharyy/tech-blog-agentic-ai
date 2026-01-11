import re
import hashlib
from services.related_block import build_related_posts_html

# ============================================================
# IMAGE CONFIG (Blogger + Mobile Safe)
# ============================================================

MAX_IMAGES_TOTAL = 4   # 1 intro + 2–3 body
IMAGE_WIDTH_DESKTOP = "720px"

def _safe_slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")

def _unique_image_url(seed_text: str) -> str:
    """
    Generates a deterministic but UNIQUE image per topic/section.
    Uses Picsum WebP (free + no copyright).
    """
    seed = int(hashlib.md5(seed_text.encode()).hexdigest()[:8], 16)
    return f"https://picsum.photos/seed/{seed}/800/450.webp"

def _image_html(src: str, alt: str) -> str:
    return f"""
    <div style="text-align:center;margin:22px 0;">
        <img src="{src}"
             alt="{alt}"
             loading="lazy"
             style="max-width:100%;width:{IMAGE_WIDTH_DESKTOP};height:auto;border-radius:8px;" />
    </div>
    """

# ============================================================
# MAIN BUILDER (COMPOSE-SAFE)
# ============================================================

def build_blog_html(structure: dict, title: str, related_posts=None) -> str:
    """
    Blogger-safe, Compose-compatible HTML builder.
    NO scripts, NO inline JS, NO title repetition.
    """

    html_parts = []
    images_used = 0

    # --------------------------------------------------------
    # INTRODUCTION
    # --------------------------------------------------------

    html_parts.append("<h2>Introduction</h2>")

    intro_text = structure.get("summary_hook") or ""
    intro_text = intro_text.strip()

    if intro_text:
        html_parts.append(f"<p><em>{intro_text}</em></p>")

        # ONE intro image ONLY
        intro_img = _unique_image_url(title)
        html_parts.append(
            _image_html(
                intro_img,
                f"{title} overview illustration"
            )
        )
        images_used += 1

    # --------------------------------------------------------
    # BODY SECTIONS
    # --------------------------------------------------------

    for section in structure.get("sections", []):

        if images_used >= MAX_IMAGES_TOTAL:
            break

        heading = section.get("heading", "").strip()
        content = section.get("content", "").strip()

        if not heading or not content:
            continue

        html_parts.append(f"<h2>{heading}</h2>")
        html_parts.append(f"<p>{content}</p>")

        # Insert ONE image per section (after first paragraph)
        if images_used < MAX_IMAGES_TOTAL:
            img_src = _unique_image_url(f"{title}-{heading}")
            html_parts.append(
                _image_html(
                    img_src,
                    f"{heading} explained"
                )
            )
            images_used += 1

        # Optional extra paragraph
        for sub in section.get("subsections", []):
            sub_text = sub.get("content", "").strip()
            if sub_text:
                html_parts.append(f"<p>{sub_text}</p>")

    # --------------------------------------------------------
    # CONCLUSION (NO IMAGE)
    # --------------------------------------------------------

    conclusion = structure.get("conclusion", "").strip()
    if conclusion:
        html_parts.append("<h2>Conclusion</h2>")
        html_parts.append(f"<p>{conclusion}</p>")

    # --------------------------------------------------------
    # CTA BUTTON
    # --------------------------------------------------------

    html_parts.append("<br><br>")
    html_parts.append("""
    <div style="text-align:center;margin-top:30px;">
        <a href="/"
           style="
             display:inline-block;
             padding:12px 26px;
             background:#1a73e8;
             color:#ffffff;
             text-decoration:none;
             border-radius:999px;
             font-weight:600;
           ">
           Check More
        </a>
    </div>
    """)

    # --------------------------------------------------------
    # RELATED POSTS (SAFE)
    # --------------------------------------------------------

    if related_posts:
        html_parts.append(build_related_posts_html(related_posts))

    return "\n".join(html_parts)
