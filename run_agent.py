import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def load_master_prompt():
    with open("master_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

def get_user_input():
    return input("Enter topic or type 'Take trending tech topic': ").strip()

def generate_canonical_article(master_prompt, user_input):
    prompt = f"""
{master_prompt}

User Input:
{user_input}

IMPORTANT:
Generate ONLY the canonical article in plain text.
Do not include HTML, markdown, bullet points, or SEO metadata.
"""

    response = client.models.generate_content(
        model="models/gemini-flash-lite-latest",
        contents=prompt
    )

    return response.text.strip()

def save_canonical_article(text):
    os.makedirs("output", exist_ok=True)
    with open("output/canonical_article.txt", "w", encoding="utf-8") as f:
        f.write(text)

def main():
    master_prompt = load_master_prompt()
    user_input = get_user_input()
    article = generate_canonical_article(master_prompt, user_input)
    save_canonical_article(article)

    print("\n✅ Agentic Brain LIVE (Gemini API connected successfully)")
    print("📄 Canonical article saved at: output/canonical_article.txt")

if __name__ == "__main__":
    main()
