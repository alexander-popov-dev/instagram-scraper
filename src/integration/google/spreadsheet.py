import logging

import gspread
from gspread import Worksheet

from src.integration.google.settings import get_google_settings

logger = logging.getLogger(__name__)

settings = get_google_settings()

class GoogleSpreadsheet:

    def __init__(self) -> None:
        self._worksheets = self._get_worksheets()

    def _get_worksheets(self) -> list[Worksheet]:
        client = gspread.authorize(credentials=settings.get_service_account)
        return client.open_by_key(settings.spreadsheed_id).worksheets()