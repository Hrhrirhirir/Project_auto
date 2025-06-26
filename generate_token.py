
from google_auth_oauthlib.flow import InstalledAppFlow
import os

SCOPES = ['https://www.googleapis.com/auth/blogger']

def main():
    creds = None
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=8080, open_browser=True)

    with open('token.json', 'w') as token:
        token.write(creds.to_json())

    print("✅ token.json created successfully!")

if __name__ == '__main__':
    main()
