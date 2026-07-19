from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Read-only access to Gmail
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

BASE_DIR = Path(__file__).resolve().parent.parent
TOKEN_FILE = BASE_DIR / "token.json"
CREDENTIALS_FILE = BASE_DIR / "credentials.json"


def authenticate():
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE),
                SCOPES
            )
            creds = flow.run_local_server(
                host="localhost",
                port=8080,
                authorization_prompt_message="Opening browser for authentication...",
                success_message="Authentication successful. You may close this window.",
                open_browser=True,
            )

        TOKEN_FILE.write_text(creds.to_json())

    return creds