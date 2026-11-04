import logging
from urllib.parse import urlparse

from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    sync_playwright,
)

from src.core.clients.base import BaseBrowserClient
from src.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class PlaywrightClient(BaseBrowserClient):
    def __init__(
        self,
        proxy: str | dict | None = None,
    ) -> None:
        self._proxy = proxy
        self._playwright: Playwright | None = None
        self._context: BrowserContext | None = None
        self._browser: Browser | None = None
        self._page: Page | None = None
        self._storage: dict | None = None

    def _get_proxy(self) -> dict | None:
        if not self._proxy:
            return None

        if isinstance(self._proxy, dict):
            return self._proxy

        parsed = urlparse(self._proxy)

        proxy = {"server": f"{parsed.scheme}://{parsed.hostname}:{parsed.port}"}

        if parsed.username:
            proxy["username"] = parsed.username

        if parsed.password:
            proxy["password"] = parsed.password

        return proxy

    def start(self, cdp_endpoint_url: str | None = None) -> None:
        self._playwright = sync_playwright().start()

        if cdp_endpoint_url:
            self._browser = self._playwright.chromium.connect_over_cdp(endpoint_url=cdp_endpoint_url)
            self._context = self._browser.contexts[0]
            self._page = self._context.pages[0]
            logger.info("Playwright over CDP successfully started")

        else:
            self._browser = self._playwright.chromium.launch(headless=settings.headless)

            self._context = self._browser.new_context()
            self._page = self._context.new_page()
            logger.info("Playwright successfully started")

    def close(self) -> None:
        if self._playwright:
            self._playwright.stop()

        logger.info("Playwright successfully stopped")

    def get_page(self) -> Page:
        return self._page
