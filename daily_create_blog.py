import os
from datetime import datetime
from auth import get_access_token
from blogger import create_blog, post_to_blogger

def main():
    access_token = get_access_token()
    today = datetime.now().strftime("%Y-%m-%d")

    blog_title = f"Daily Blog {today}"
    blog_description = f"This blog was automatically created on {today}"

    blog_id = create_blog(blog_title, blog_description, access_token)

    title = f"Welcome - {today}"
    content = f"<p>This is the daily start post for {today}. Stay tuned!</p>"
    labels = [today]

    post_to_blogger(blog_id, title, content, access_token, labels)

    # لو حبيت تحتفظ بالـ blog_id لاستخدامه في post later
    print(f"📌 BLOG_ID={blog_id}")

if __name__ == "__main__":
    main()
# هذا سطر فقط لتحديث الملف وإجبار GitHub على قراءته من جديد
