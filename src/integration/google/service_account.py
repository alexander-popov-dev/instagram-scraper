from google.oauth2.service_account import Credentials
from google.oauth2.sts import Client

from src.integration.google.settings import get_google_settings

settings = get_google_settings()
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


class ServiceAccount:

    @classmethod
    def create(cls) -> Client:
        return Credentials.from_service_account_file(settings.service_account_creds_path, scopes=SCOPES)
