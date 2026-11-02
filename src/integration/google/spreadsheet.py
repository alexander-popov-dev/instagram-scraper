import gspread
from google.oauth2.service_account import Credentials
from gspread import Worksheet

class GoogleSpreadsheet:

    def __init__(self, service_account: Credentials, spreadsheet_id: str) -> None:
        self._service_account = service_account
        self._spreadsheet_id = spreadsheet_id
        self.worksheets: list[Worksheet] = self.__get_worksheets()

    def __get_worksheets(self) -> list[Worksheet]:
        client = gspread.authorize(credentials=self._service_account)
        return client.open_by_key(key=self._spreadsheet_id).worksheets()
