import os
import re

CANONICAL_PATH = "output/canonical_article.txt"
BLOGGER_HTML_PATH = "output/blogger.html"
WORDPRESS_HTML_PATH = "output/wordpress.html"


def read_canonical():
    if not os.path.exists(CANONICAL_PATH):
        raise FileNotFoundError("canonical_article.txt not found")

    with open(CANONICAL_PATH, "r", encoding="utf-8") as f:
        return f.read().strip()


def convert_to_html(text, wordpress=False):
    lines = text.split("\n")

    html = []
    in_ul = False
    in_ol = False
    h1_used = False

    def wp(block):
        return f"<!-- wp:{block} -->"

    def wp_end(block):
        return f"<!-- /wp:{block} -->"

    for raw_line in lines:
        line = raw_line.strip()

        if line == "":
            if in_ul:
                html.append("</ul>")
                if wordpress:
                    html.append(wp_end("list"))
                in_ul = False
            if in_ol:
                html.append("</ol>")
                if wordpress:
                    html.append(wp_end("list"))
                in_ol = False
            continue

        if not h1_used:
            if wordpress:
                html.append(wp("heading"))
                html.append(f"<h1>{line}</h1>")
                html.append(wp_end("heading"))
            else:
                html.append(f"<h1>{line}</h1>")
            h1_used = True
            continue

        if line.startswith("## "):
            title = line[3:].strip()
            if wordpress:
                html.append(wp("heading"))
                html.append(f"<h2>{title}</h2>")
                html.append(wp_end("heading"))
            else:
                html.append(f"<h2>{title}</h2>")

            html.append("<!-- IMAGE SLOT -->")
            html.append(f"<!-- Image prompt: {title} concept illustration -->")
            html.append(f"<!-- ALT text: {title} explained visually -->")
            continue

        if line.startswith("### "):
            if wordpress:
                html.append(wp("heading"))
                html.append(f"<h3>{line[4:].strip()}</h3>")
                html.append(wp_end("heading"))
            else:
                html.append(f"<h3>{line[4:].strip()}</h3>")
            continue

        if line.startswith("- ") or line.startswith("• "):
            if not in_ul:
                if wordpress:
                    html.append(wp("list"))
                html.append("<ul>")
                in_ul = True
            html.append(f"<li>{line[2:].strip()}</li>")
            continue

        if re.match(r"^\d+\.\s", line):
            if not in_ol:
                if wordpress:
                    html.append(wp("list"))
                html.append("<ol>")
                in_ol = True
            html.append(f"<li>{line.split('.', 1)[1].strip()}</li>")
            continue

        if wordpress:
            html.append(wp("paragraph"))
            html.append(f"<p>{line}</p>")
            html.append(wp_end("paragraph"))
        else:
            html.append(f"<p>{line}</p>")

    return "\n".join(html)


def save_html(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    text = read_canonical()

    blogger_html = convert_to_html(text, wordpress=False)
    wordpress_html = convert_to_html(text, wordpress=True)

    save_html(BLOGGER_HTML_PATH, blogger_html)
    save_html(WORDPRESS_HTML_PATH, wordpress_html)

    print("✅ Blogger + WordPress HTML generated")
    print("📄 Blogger HTML → output/blogger.html")
    print("📄 WordPress HTML → output/wordpress.html")


if __name__ == "__main__":
    main()

