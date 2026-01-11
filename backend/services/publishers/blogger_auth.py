from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import json
import os

SCOPES = ["https://www.googleapis.com/auth/blogger"]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CREDENTIALS_DIR = os.path.join(BASE_DIR, "credentials")

CLIENT_SECRET_FILE = os.path.join(CREDENTIALS_DIR, "client_secret.json")
TOKEN_FILE = os.path.join(CREDENTIALS_DIR, "blogger_token.json")


def generate_token():
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        SCOPES
    )

    creds = flow.run_local_server(port=0)

    with open(TOKEN_FILE, "w") as token:
        token.write(creds.to_json())

    print("✅ Blogger OAuth token generated successfully")


if __name__ == "__main__":
    generate_token()
