import asyncio
import json
import logging

from src.platforms.instagram.reels.service import ReelsService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    with open("../accounts.json", "r", encoding="utf-8") as file:
        accounts = json.load(file)

    service = ReelsService()
    for account in accounts:
        logger.info(f"Account {account['name']} started")
        await service.collect_reels_data(profile_id=account["profile_id"])
        logger.info(f"Account {account['name']} finished")


if __name__ == '__main__':
    asyncio.run(main())

