from src.integration.google.spreadsheet import GoogleSpreadsheet
from src.platforms.instagram.reels.schemas import Reel
from src.platforms.instagram.reels.storages.base import BaseReelStorage
from src.platforms.instagram.settings import get_reels_settings


class ReelSpreadsheet(BaseReelStorage):

    def __init__(self) -> None:
        self._settings = get_reels_settings()
        self._worksheets = GoogleSpreadsheet(
            service_account=self._settings.get_service_account,
            spreadsheet_id=self._settings.spreadsheet_id,
        )
        self._reels_spreadsheet = self._worksheets.worksheets[0]

    def get_all_reels(self) -> list[Reel]:
        records = self._reels_spreadsheet.get_all_values()
        return [Reel.model_validate(record) for record in records if records[0]]


    def save_reels(self, reels: list[Reel]):
        saved_reels = self.get_all_reels()
        print(reels[0].model_fields)
        if not saved_reels:
            rows = [[row for row in reels[0].model_fields]]
            self._reels_spreadsheet.insert_rows(rows)
