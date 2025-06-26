import requests
from auth import get_access_token
from datetime import datetime
def post_to_blogger(blog_id, title, content, labels=None):
    access_token = get_access_token()
    url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "kind": "blogger#post",
        "title": title,
        "content": content
    }
    if labels:
        data["labels"] = labels

    response = requests.post(url, headers=headers, json=data)

    if response.status_code in [200, 201]:
        post = response.json()
        print(f"✅ Post published: {post['title']} | ID: {post['id']}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
