import random
from functools import cache
from pathlib import Path

from google.oauth2.service_account import Credentials

from src.settings import BaseProjectSettings


class ReelsProjectSettings(BaseProjectSettings):
    spreadsheet_id: str
    service_account_creds_path: Path = Path(__file__).resolve().parents[3] / 'service_account.json'
    scopes: list = [
        "https://www.googleapis.com/auth/spreadsheets"
    ]

    # Run criteria
    max_scrolls_count: int
    min_scrolls_count: int
    max_pause_interval_minutes: int
    min_pause_interval_minutes: int

    # Reels criteria
    min_reports_count: int
    max_reel_age_days: int
    max_days_to_keep_reels: int

    @property
    def scrolls_count(self) -> int:
        return random.randint(self.min_scrolls_count, self.max_scrolls_count)

    @property
    def pause_interval_minutes(self) -> int:
        return random.randint(self.min_pause_interval_minutes, self.max_pause_interval_minutes)

    @property
    def get_service_account(self):
        return Credentials.from_service_account_file(
            filename=str(self.service_account_creds_path),
            scopes=self.scopes
        )


@cache
def get_reels_settings() -> ReelsProjectSettings:
    return ReelsProjectSettings()
