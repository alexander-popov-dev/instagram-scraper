import random

from playwright.async_api import Page, async_playwright, Response

from src.providers.nst import NstBrowserProvider


class ReelsScraper:
    def __init__(self) -> None:
        self._page: Page | None = None
        self._provider: NstBrowserProvider = NstBrowserProvider()
        self._raw_data: list[dict] | None = None

    async def _on_response(self, response: Response):
        if "/api/graphql" in response.url and response.request.method == "POST":
            if "xdt_api__v1__clips__home__connection_v2" in await response.text():
                print(await response.json())

    async def _key_scroll(self) -> None:
        for _ in range(30):
            await self._page.keyboard.press("ArrowDown")
            await self._page.wait_for_timeout(random.uniform(2000, 10000))

    async def _wheel_scroll(self) -> None:
        for _ in range(30):
            await self._page.bring_to_front()
            vp = self._page.viewport_size or {"width": 1280, "height": 800}
            await self._page.mouse.move(vp["width"] / 2, vp["height"] / 2)

    async def scrape(self):
        async with async_playwright() as playwright:
            browser = await playwright.chromium.connect_over_cdp(endpoint_url=self._provider.get_local_endpoint_url())
            context = browser.contexts[0]
            self._page = context.pages[0]
            self._page.on("response", self._on_response)

            await self._key_scroll()
