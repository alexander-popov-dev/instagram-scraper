from functools import cache
from pathlib import Path

from google.oauth2.service_account import Credentials

from src.settings import BaseProjectSettings


class GoogleProjectSettings(BaseProjectSettings):
    spreadsheed_id: str
    service_account_creds_path: Path = Path(__file__).resolve().parent.parent.parent / 'service_account.json'
    scopes: list = [
        "https://www.googleapis.com/auth/spreadsheets"
    ]

    @property
    def get_service_account(self):
        return Credentials.from_service_account_file(
            filename=self.service_account_creds_path,
            scopes=self.scopes
        )


@cache
def get_google_settings() -> GoogleProjectSettings:
    return GoogleProjectSettings()
