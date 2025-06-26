import os
import time
import re
import urllib.parse
from utils import is_duplicate, save_posted_title
import requests
from topic_generator import get_trending_topic
from blogger import post_to_blogger
from meta_generator import generate_meta_description
# إعداد متغيرات البيئة
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BLOG_ID = os.getenv("BLOG_ID") 

# دالة توليد Access Token من Google
def get_access_token():
    print("🔐 Getting access token from Google...")
    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token"
    }

    try:
        res = requests.post(token_url, data=payload)
        res.raise_for_status()
        access_token = res.json().get("access_token")
        return access_token
    except Exception as e:
        print("❌ Error getting access token:", e)
        return None

# دالة توليد مقال باستخدام Gemini
def generate_article(topic: str) -> str:
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key=AIzaSyDSOgakd0CgLzG0h8C1ZXIjMV7OavNax9c"
    
    headers = {
        "Content-Type": "application/json"
    }

    prompt = f"""Write a detailed and informative blog post about: {topic}.It should be informative, engaging, and formatted well.
 Use:
- A friendly introduction
- Exclusive content, high value content
- Clear subheadings, Write the sources under the blog only. 
- Natural tone and smooth flow,  Write without symbols between words or subtitles.
- Short paragraphs, Dive into the information and make it influential.
- A personal or reflective conclusion, Write creatively, discuss and compare like make  tables. 
Avoid robotic language, repetition, or markdown. Output plain text only. Around 700-800 words."""
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        print("❌ Error generating article with Gemini:", e)
        return "This is a default article content due to an error in generating the article."
        
def get_image_html(topic: str) -> str:
    safe_topic = re.sub(r"[^\w\s]", "", topic)  # إزالة الرموز مثل % و ’ و –
    query = urllib.parse.quote(f"{safe_topic}, digital art, 800x400") 
    image_url = f"https://image.pollinations.ai/prompt/{query}"

    for attempt in range(3):
        try:
            print(f"🖼️ محاولة تحميل الصورة رقم {attempt + 1}")
            response = requests.get(image_url, timeout=19)

            if response.status_code == 200 and "image" in response.headers.get("Content-Type", ""):
                return f'''
                <img src="{image_url}" alt="{topic}" 
                style="width:100%;max-width:800px;height:auto;
                aspect-ratio:2/1;border-radius:12px;margin-bottom:15px;">
                '''
        except Exception as e:
            print(f"⚠️ محاولة {attempt + 1} فشلت: {e}")
            time.sleep(2)

    print("❌ فشل تحميل الصورة بعد 3 محاولات")
    return '''
    <img src="https://via.placeholder.com/800x400?text=Image+Error" alt="Error Image" 
    style="width:100%;max-width:800px;height:auto;aspect-ratio:2/1;
    border-radius:12px;margin-bottom:15px;">
    '''

def format_article(article: str, title: str) -> str:
    # 🔧 تنظيف الرموز الغريبة والتنسيقات
    article = re.sub(r"[\u200B-\u200D\uFEFF]", "", article)  # رموز غير مرئية
    article = re.sub(r"#\w+", "", article)  # إزالة الهاشتاقات
    article = re.sub(r"[^\x00-\x7F]+", " ", article)  # إزالة رموز غير ASCII
    article = re.sub(r"\*{1,2}(.*?)\*{1,2}", r"\1", article)
    article = re.sub(r"\_{1,2}(.*?)\_{1,2}", r"\1", article)
    article = re.sub(r"^\s*>\s*", "", article, flags=re.MULTILINE)
    article = re.sub(r".*?.*?", "", article)
    article = re.sub(r"\!.*?.*?", "", article)
    article = re.sub(r".*?", "", article)
    article = re.sub(r"---+", "", article)
    article = re.sub(r"\*\s+", "", article)
    article = re.sub(r"(?m)^\s{0,3}#{1,6}\s*", "", article)
    article = article.encode('ascii', 'ignore').decode('ascii')  # إزالة أي رمز غير ASCII

    paragraphs = article.split("\n")
    formatted_paragraphs = []

    # تعريف دالة لاختيار العناوين الفرعية
    def is_subheading(p: str) -> bool:
        words = p.split()
        if len(words) > 10:
            return False

        starts_with_cap = p[0].isupper()
        ends_without_punct = not p.strip().endswith(('.', '!', '?'))
        has_few_verbs = not re.search(r"\b(is|are|was|were|have|has|had|do|does|did|can|should|could)\b", p, re.IGNORECASE)
        contains_heading_keywords = re.search(
            r"\b(introduction|summary|conclusion|overview|benefits|pros|cons|tips|steps|key points|examples|how to|why|what is|types|guide|reasons|methods|strategies|final thoughts)\b",
            p,
            re.IGNORECASE,
        )

        score = sum([
            starts_with_cap,
            ends_without_punct,
            has_few_verbs,
            bool(contains_heading_keywords)
        ])

        return score >= 2  # على الأقل شرطين متحققين

    # تنسيق الفقرات باستخدام دالة is_subheading
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue

        if is_subheading(p):
            formatted_paragraphs.append(
                f'<h3 style="color:#2c3e50;font-size:20px;margin-top:30px;margin-bottom:15px;font-weight:bold;font-family:Arial,sans-serif;">{p}</h3>'
            )
        else:
            formatted_paragraphs.append(
                f'<p style="margin:15px 0;line-height:1.8;font-size:17px;color:#333;font-family:Arial,sans-serif;">{p}</p>'
            )

    # 🖼️ إضافة صورة أول المقال
    image_html = get_image_html(title)
    if not title.strip() or len(title.strip()) < 4:
        title = "Path to Grow"

    # 📦 تجميع المقال النهائي
    formatted_article = f'''
    <div style="text-align:center;margin-bottom:20px;">
        {image_html}
        <h2 style="margin-top:10px;font-size:28px;color:#2c3e50;font-family:Arial,sans-serif;">{title}</h2>
    </div>
    <div style="padding:10px;">
        {''.join(formatted_paragraphs)}
    </div>
    <hr style="margin-top:30px;">
    '''
    return formatted_article


# الدلة الرئيسية
def main():
    if not os.path.exists("posted_articles.json"):
        with open("posted_articles.json", "w", encoding="utf-8") as f:
            json.dump([], f)
        print("📄 Created empty posted_articles.json")

    topic = get_trending_topic()
    print(f"✍️ توليد مقال عن: {topic}")
    
    if is_duplicate(topic):
        print(f"⚠️ المقال '{topic}' تم نشره سابقًا. سيتم تجاهله.")
        return  # يوقف التنفيذ

    article = generate_article(topic)
    meta_description = generate_meta_description(topic, article)
    formatted_article = format_article(article, topic)
    access_token = get_access_token()

    if access_token:
        post_to_blogger(BLOG_ID, topic, formatted_article, access_token, meta_description=meta_description)
        save_posted_title(topic)
    else:
        print("❌ Failed to get access token. Skipping post.")

if __name__ == "__main__":
    main() 
