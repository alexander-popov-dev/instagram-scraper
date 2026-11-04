from nstbrowser import NstbrowserClient

from src.core.providers.base import BaseBrowserProvider


class NstBrowserProvider(BaseBrowserProvider):

    def __init__(self, api_key: str) -> None:
        self._client = NstbrowserClient(api_key=api_key)

    def start(self, profile_id: str) -> str:
        response = self._client.browsers.start_browser(profile_id=profile_id)
        return f'http://127.0.0.1:{response["data"]["port"]}'

    def stop(self, profile_id: str) -> None:
        self._client.browsers.stop_browser(profile_id=profile_id)
