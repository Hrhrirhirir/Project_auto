import json
import os
import re

POSTED_FILE_PATH = "posted_articles.json"
print(f"Using posted articles file at: {POSTED_FILE_PATH}")

def normalize_title(title: str) -> str:
    title = title.lower().strip()
    title = re.sub(r"[^\w\s]", "", title)
    title = re.sub(r"\s+", " ", title)
    return title

def load_posted_titles():
    if os.path.exists(POSTED_FILE_PATH):
        with open(POSTED_FILE_PATH, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_posted_title(title):
    posted = load_posted_titles()
    normalized_title = normalize_title(title)
    if normalized_title not in posted:
        posted.append(normalized_title)
        with open(POSTED_FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(posted, file, ensure_ascii=False, indent=2)
        print(f"✅ Saved title to {POSTED_FILE_PATH}")
    else:
        print(f"ℹ️ Title already exists: {normalized_title}")

def is_duplicate(title):
    normalized_title = normalize_title(title)
    return normalized_title in load_posted_titles()
