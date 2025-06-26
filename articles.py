import requests

def create_blog(title, description, access_token):
    url = 'https://www.googleapis.com/blogger/v3/users/self/blogs'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        "kind": "blogger#blog",
        "name": title,
        "description": description,
        "locale": {
            "language": "en",
            "country": "US"
        }
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200 or response.status_code == 201:
        blog = response.json()
        print(f"Created blog: {blog['name']} (ID: {blog['id']})")
        return blog['id']
    else:
        raise Exception(f"Failed to create blog: {response.text}")

def post_to_blogger(blog_id, title, content, access_token, labels=None, meta_description=None):
    url = f'https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    post_data = {
        'kind': 'blogger#post',
        'title': title,
        'content': content,
    }
    if meta_description:
        post_data['postMetaDescription'] = meta_description
    if labels:
        post_data['labels'] = labels

    response = requests.post(url, json=post_data, headers=headers)
    if response.status_code == 200 or response.status_code == 201:
        post = response.json()
        print(f"Posted article titled '{post['title']}' with ID {post['id']}")
        return post['id']
    else:
        raise Exception(f"Failed to post article: {response.text}")





