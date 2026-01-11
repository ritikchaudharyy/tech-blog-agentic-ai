from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
from datetime import datetime

from backend.services.publishers.base import BasePublisher


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CREDENTIALS_DIR = os.path.join(BASE_DIR, "credentials")

TOKEN_FILE = os.path.join(CREDENTIALS_DIR, "blogger_token.json")

SCOPES = ["https://www.googleapis.com/auth/blogger"]


class BloggerPublisher(BasePublisher):

    def _get_service(self):
        if not os.path.exists(TOKEN_FILE):
            raise RuntimeError("Blogger token not found. Run blogger_auth first.")

        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

        # 🔐 Auto refresh token
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(TOKEN_FILE, "w") as f:
                f.write(creds.to_json())

        return build("blogger", "v3", credentials=creds)

    def get_blog_id(self):
        service = self._get_service()
        blogs = service.blogs().listByUser(userId="self").execute()

        if not blogs.get("items"):
            raise RuntimeError("No Blogger blogs found")

        return blogs["items"][0]["id"]

    def publish(self, article):
        service = self._get_service()
        blog_id = self.get_blog_id()

        body = {
            "kind": "blogger#post",
            "title": article.title,  # Blogger title only
            "content": article.canonical_content,  # ✅ CORRECT FIELD
            "labels": article.seo_tags.split(",") if article.seo_tags else []
        }

        post = service.posts().insert(
            blogId=blog_id,
            body=body,
            isDraft=False
        ).execute()

        return {
            "post_id": post["id"],
            "url": post["url"],
            "status": "published",
            "published_at": datetime.utcnow().isoformat()
        }
