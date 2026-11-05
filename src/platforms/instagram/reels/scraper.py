import json
import logging
import random
from typing import Callable, Awaitable

from playwright.async_api import Response

from src.core.clients.browser.playwright.client import PlaywrightClient, logger
from src.platforms.instagram.reels.exceptions import ReelsBatchException


class ReelsScraper(PlaywrightClient):
    def __init__(
            self,
            cdp_endpoint_url: str | None,
            on_batch: Callable[[dict], Awaitable[None]],
            scrolls_count: int = 100,
    ) -> None:
        super().__init__(cdp_endpoint_url=cdp_endpoint_url)
        self._on_batch = on_batch
        self._scrolls_count = scrolls_count
        self._raw_data: list[dict] | None = None
        self._current_batch_count: int = 0

    async def _on_response(self, response: Response):
        if "/api/graphql" not in response.url or response.request.method != "POST":
            return

        try:
            text = await response.text()
            if "xdt_api__v1__clips__home__connection_v2" not in text:
                return

            data_json = json.loads(text)
        except Exception as e:
            raise ReelsBatchException("Couldn't parse json", e)

        await self._on_batch(data_json)
        self._current_batch_count += 1
        logging.info(f"Scraped reels batch: {self._current_batch_count}")

    async def _key_scroll(self) -> None:
        for i in range(self._scrolls_count):
            logger.info(f"Scroll: {i + 1}/{self._scrolls_count}")
            await self._page.keyboard.press("ArrowDown")
            await self._page.wait_for_timeout(random.uniform(2000, 10000))

    async def _wheel_scroll(self) -> None:
        for i in range(self._scrolls_count):
            logger.info(f"Scroll: {i + 1}/{self._scrolls_count}")
            await self._page.bring_to_front()
            vp = self._page.viewport_size or {"width": 1280, "height": 800}
            await self._page.mouse.move(vp["width"] / 2, vp["height"] / 2)

    async def scrape(self):
        try:
            self._page.on("response", self._on_response)
            await self._key_scroll()
        finally:
            self._page.remove_listener("response", self._on_response)
