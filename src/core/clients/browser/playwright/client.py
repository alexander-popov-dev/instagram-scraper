import logging
from urllib.parse import urlparse

from playwright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    async_playwright,
)

from src.core.clients.base import BaseBrowserClient
from src.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class PlaywrightClient(BaseBrowserClient):
    def __init__(
            self,
            proxy: str | dict | None = None,
            cdp_endpoint_url: str | None = None
    ) -> None:
        self._proxy = proxy
        self._cdp_endpoint_url = cdp_endpoint_url
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

    async def start(self) -> None:
        self._playwright = await async_playwright().start()

        if self._cdp_endpoint_url:
            self._browser = await self._playwright.chromium.connect_over_cdp(endpoint_url=self._cdp_endpoint_url)
            self._context = self._browser.contexts[0]
            self._page = self._context.pages[0]
            logger.info("Playwright over CDP successfully started")

        else:
            self._browser = await self._playwright.chromium.launch(headless=False)
            self._context = await self._browser.new_context(proxy=self._get_proxy())
            self._page = await self._context.new_page()
            logger.info("Playwright successfully started")

    async def close(self) -> None:
        if self._playwright:
            await self._playwright.stop()

        logger.info("Playwright successfully stopped")

    async def get_page(self) -> Page:
        if not self._page:
            raise RuntimeError("Playwright not started yet")

        return self._page
