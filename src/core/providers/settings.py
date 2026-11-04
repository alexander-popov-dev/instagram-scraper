from functools import cache

from src.settings import BaseProjectSettings


class ProvidersProjectSettings(BaseProjectSettings):
    nst_api_key: str
    nst_profile_id: str


@cache
def get_providers_settings() -> ProvidersProjectSettings:
    return ProvidersProjectSettings()
