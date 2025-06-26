import re

def generate_meta_description(title: str, article: str) -> str:
    # تنظيف المقال من الرموز والعلامات
    article = re.sub(r"[\n\r]", " ", article)
    article = re.sub(r"<.*?>", "", article)  # إزالة الوسوم HTML
    article = re.sub(r"\s+", " ", article).strip()

    # أخذ أول جملة مفيدة مناسبة
    sentences = re.split(r"(?<=[.!?])\s+", article)
    for sentence in sentences:
        if 40 <= len(sentence) <= 160:
            return sentence

    # fallback: توليد وصف يدوي إذا لم تُستخرج جملة مناسبة
    return f"{title.strip().capitalize()} - Learn more about this topic in a concise and informative article."

# مثال:
if __name__ == "__main__":
    title = "Moving Toward Circular Agriculture"
    article = """
    Circular agriculture is a modern approach that emphasizes sustainability. 
    It minimizes waste by reusing resources and integrating livestock with crop production. 
    Farmers and researchers are exploring these practices to ensure food security for the future.
    """
    meta = generate_meta_description(title, article)
    print("✅ Meta Description:\n", meta)
