import os
import json

CANONICAL_PATH = "output/canonical_article.txt"
SEO_OUTPUT_PATH = "output/seo_package.json"


def read_canonical():
    if not os.path.exists(CANONICAL_PATH):
        raise FileNotFoundError("canonical_article.txt not found")

    with open(CANONICAL_PATH, "r", encoding="utf-8") as f:
        return f.read()


def generate_meta_description(text):
    sentences = text.replace("\n", " ").split(".")
    meta = sentences[0].strip()
    return meta[:157] + "..." if len(meta) > 160 else meta


def generate_tags(text):
    keywords = [
        "On-device AI",
        "AI laptops",
        "Future of computing",
        "Neural Processing Unit",
        "AI hardware",
        "Laptop technology"
    ]
    return keywords


def generate_internal_links():
    return [
        "Best laptops for students in 2025",
        "Cloud AI vs On-device AI explained",
        "ARM vs x86 processors for laptops"
    ]


def main():
    text = read_canonical()

    seo_package = {
        "meta_description": generate_meta_description(text),
        "tags": generate_tags(text),
        "internal_links": generate_internal_links()
    }

    with open(SEO_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(seo_package, f, indent=2)

    print("✅ SEO package generated")
    print("📄 Saved to:", SEO_OUTPUT_PATH)


if __name__ == "__main__":
    main()
