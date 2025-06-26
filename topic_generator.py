import requests
import random
from bs4 import BeautifulSoup
from utils import is_duplicate

fallback_topics = [
    "Artificial Intelligence 2025",
    "Climate Change Effects",
    "SpaceX Mars Mission",
    "Cryptocurrency Regulations",
    "iPhone 17 Rumors",
    "New Electric Cars 2025",
    "Best AI Tools This Year",
    "Future of Work in AI Era",
    "Mental Health Awareness Trends",
    "Clean Energy Innovations"
]

def get_bing_trending_topics():
    try:
        url = "https://www.bing.com/news/topicview" 
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        topics = [a.get_text(strip=True) for a in soup.select("a.title")]

        return topics if topics else []
    except Exception as e:
        print("❌ Error fetching Bing Trends:", e)
        return []

def get_trending_topic():
    try:
        topics = get_bing_trending_topics()
        if topics:
            random.shuffle(topics)
            for topic in topics:
                if not is_duplicate(topic):
                    return topic
            print("⚠️ All trending topics were already used. Using fallback.")
    except Exception as e:
        print("❌ Error getting trending topic:", e)

    # إذا فشل كل شيء، اختر من القائمة الاحتياطية وتجنب التكرار
    fallback_available = [t for t in fallback_topics if not is_duplicate(t)]
    if fallback_available:
        return random.choice(fallback_available)
    else:
        return random.choice(fallback_topics)  # fallback نهائي حتى لو مكرر
