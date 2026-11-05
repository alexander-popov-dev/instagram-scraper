import logging
from datetime import datetime, timedelta, timezone

from src.integration.google.spreadsheet import GoogleSpreadsheet
from src.platforms.instagram.reels.schemas import Reel
from src.platforms.instagram.reels.storages.base import BaseReelStorage
from src.platforms.instagram.settings import get_reels_settings

logger = logging.getLogger(__name__)


class ReelSpreadsheetStorage(BaseReelStorage):

    def __init__(self) -> None:
        self._settings = get_reels_settings()
        self._worksheets = GoogleSpreadsheet(
            service_account=self._settings.service_account,
            spreadsheet_id=self._settings.spreadsheet_id,
        )
        self._reels_spreadsheet = self._worksheets.worksheets[0]

    def get_all_reels(self) -> list[Reel] | None:
        records = self._reels_spreadsheet.get_all_values(pad_values=True)

        if not records or len(records) <= 1:
            return None

        headers = records[0]
        data_rows = records[1:]

        reels: list[Reel] = []
        for row in data_rows:
            if not any(row):
                continue

            row_dict = {col: val for col, val in zip(headers, row) if col}
            reels.append(Reel.model_validate(row_dict))

        return reels if reels else None

    def save_reels(self, reels: list[Reel]) -> None:
        records = self._reels_spreadsheet.get_all_values(pad_values=True)

        self._add_headers(records=records, reels=reels)
        self._save_records(records=records, reels=reels)

    def delete_old_reels(self, max_days: int) -> None:
        records = self._reels_spreadsheet.get_all_values(pad_values=True)

        if not records or len(records) <= 1:
            return

        headers = records[0]
        data_rows = records[1:]

        try:
            date_col_idx = headers.index("collected_at")
        except ValueError:
            raise ValueError("Column collected_at not found")

        threshold_date = datetime.now(tz=timezone.utc) - timedelta(days=max_days)

        filtered_rows = []
        for row in data_rows:
            if not any(row):
                continue

            date_str = row[date_col_idx]
            if not date_str:
                continue

            try:
                reel_date = datetime.fromisoformat(date_str)
                if reel_date >= threshold_date:
                    filtered_rows.append(row)

            except Exception:
                logger.error(f"Failed to parse date {date_str}")
                continue

        if len(filtered_rows) < len(data_rows):
            self._reels_spreadsheet.clear()
            self._reels_spreadsheet.update([headers] + filtered_rows)
            logger.info(f"Deleted old reels: {len(data_rows)} - {len(filtered_rows)}")

    def _save_records(self, records: list, reels: list[Reel]) -> None:
        exists_reels = [record[4] for record in records if record and record[4]]
        rows = [list(reel.model_dump(mode="json").values()) for reel in reels if reel.url not in exists_reels]

        if rows:
            self._reels_spreadsheet.append_rows(rows)
            logger.info(f"Saved {len(rows)} reels")

    def _add_headers(self, records: list, reels: list[Reel]) -> None:
        if not records or len(records[0]) == 0:
            headers = list(reels[0].model_fields.keys())

            self._reels_spreadsheet.insert_rows([headers])
            logger.info("Headers added")
