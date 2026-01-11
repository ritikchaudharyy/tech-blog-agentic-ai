import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
PROMPT_PATH = os.path.join(BASE_DIR, "master_prompt.txt")

def load_master_prompt():
    if not os.path.exists(PROMPT_PATH):
        raise FileNotFoundError(f"master_prompt.txt not found at {PROMPT_PATH}")

    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()

