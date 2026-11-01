from src.platforms.instagram.reels.parser import ReelsParser
from src.platforms.instagram.reels.scraper import ReelsScraper


class InstagramService:
    def __init__(self, scraper: ReelsScraper, parser: ReelsParser):
        self._scraper = scraper
        self._parser = parser

    async def collect_reels_data(self) -> None:
        await self._scraper.scrape()
