import asyncio
import json
import logging
from datetime import datetime, timedelta, timezone

from src.core.notifications.telegram import TelegramManager
from src.platforms.instagram.reels.service import ReelsService
from src.platforms.instagram.settings import get_reels_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
settings = get_reels_settings()


async def process_account(account: dict) -> None:
    profile_id = account["profile_id"]
    account_name = account["name"]
    telegram = TelegramManager()

    while True:
        try:
            logger.info(f"Account {account_name} started")

            service = ReelsService()
            await service.collect_reels_data(profile_id=profile_id)

            logger.info(f"Account {account_name} finished")

        except Exception as e:
            msg = f"Error in account {account_name}: {e}"
            logger.error(msg)
            telegram.send_message(message=msg)

        pause_minutes = settings.pause_interval_minutes
        start = datetime.now(tz=timezone.utc) + timedelta(minutes=pause_minutes)

        while True:
            now = datetime.now(tz=timezone.utc)
            if now < start:
                remaining = start - now
                logger.info(f"Account {account_name} next run after {remaining}")
                await asyncio.sleep(30)
                continue
            break


async def main() -> None:
    with open("../accounts.json", "r", encoding="utf-8") as file:
        accounts = json.load(file)

    if not accounts:
        logger.warning("No accounts found in accounts.json")
        return

    logger.info(f"Starting pipeline for {len(accounts)} accounts asynchronously...")

    tasks = [process_account(account) for account in accounts]

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())