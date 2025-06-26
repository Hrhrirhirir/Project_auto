import os
import requests

def get_access_token():
    refresh_token = os.environ.get('REFRESH_TOKEN')
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')

    if not all([refresh_token, client_id, client_secret]):
        raise Exception("❌ Missing one or more required environment variables: REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET")

    token_url = 'https://oauth2.googleapis.com/token'
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
    }

    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        if not access_token:
            raise Exception("❌ Failed to get access_token from response.")
        return access_token
    else:
        raise Exception(f"❌ Failed to refresh token: {response.status_code} - {response.text}")
