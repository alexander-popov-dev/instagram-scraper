from nstbrowser import NstbrowserClient

from src.providers.settings import get_providers_settings

settings = get_providers_settings()


class NstBrowserProvider:

    def __init__(self) -> None:
        self._client = NstbrowserClient(api_key=settings.nst_api_key)

    def get_local_endpoint_url(self) -> str:
        response = self._client.browsers.start_browser(profile_id=settings.nst_profile_id)
        return f'http://127.0.0.1:{response["data"]["port"]}'
