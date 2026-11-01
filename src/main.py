import asyncio

from src.platforms.instagram.reels.scraper import ReelsScraper


async def main():
    scraper = ReelsScraper()
    await scraper.scrape()

if __name__ == '__main__':
    asyncio.run(main())

