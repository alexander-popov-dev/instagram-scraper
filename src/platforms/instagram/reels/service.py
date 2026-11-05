import asyncio
import logging
from asyncio import Queue
from datetime import datetime, timezone, timedelta

from src.core.notifications.telegram import TelegramManager
from src.core.providers.nst.provider import NstBrowserProvider
from src.core.providers.settings import get_providers_settings
from src.platforms.instagram.reels.parser import ReelsParser
from src.platforms.instagram.reels.schemas import Reel
from src.platforms.instagram.reels.scraper import ReelsScraper
from src.platforms.instagram.reels.storages.spreadsheet import ReelSpreadsheetStorage
from src.platforms.instagram.settings import get_reels_settings

providers_settings = get_providers_settings()
reels_settings = get_reels_settings()
logger = logging.getLogger(__name__)


class ReelsService:
    def __init__(self):
        self._scraper = ReelsScraper
        self._parser = ReelsParser()
        self._storage = ReelSpreadsheetStorage()
        self._telegram = TelegramManager()


    async def _consume(self, queue: Queue[dict | None]) -> None:
        while raw := await queue.get():
            if not raw:
                break

            reels = self._parser.parse(raw)

            if reels:
                reels = await self._filter_by_criteria(reels=reels)
                await asyncio.to_thread(self._storage.save_reels, reels)

    async def _filter_by_criteria(self, reels: list[Reel]) -> list[Reel]:
        filtered_reels = []
        threshold_date = datetime.now(tz=timezone.utc) - timedelta(days=reels_settings.max_reel_age_days)
        for reel in reels:

            if reel.repost_count < reels_settings.min_reports_count:
                continue

            if reel.like_count < reels_settings.min_likes_count:
                continue

            if reel.comment_count < reels_settings.min_comments_count:
                continue

            if reel.taken_at < threshold_date:
                continue

            filtered_reels.append(reel)

            logger.info(
                f"Saved Reel: ID: {reel.media_id}, URL: {reel.url} "
                f"Reposts: {reel.repost_count}, Likes: {reel.like_count},  Comments: {reel.comment_count}"
            )

        return filtered_reels

    async def collect_reels_data(self, profile_id: str) -> None:
        provider = NstBrowserProvider(api_key=providers_settings.nst_api_key)
        cdp_endpoint_url = provider.start(profile_id=profile_id)
        scroll_count = reels_settings.scrolls_count

        logger.info(f"Scroll count {scroll_count}")

        queue = asyncio.Queue()
        worker = asyncio.create_task(self._consume(queue=queue))

        try:
            async with self._scraper(
                    cdp_endpoint_url=cdp_endpoint_url,
                    on_batch=queue.put,
                    scrolls_count=scroll_count,
            ) as scraper:
                await scraper.scrape()

        except Exception as e:
            msg = f"Failed to scrape reels data: {str(e)}"
            logger.exception(msg)
            self._telegram.send_message(message=f"Instagram:\n{msg}")

        finally:
            await queue.put(None)
            await worker
            self._storage.delete_old_reels(max_days=reels_settings.max_days_to_keep_reels)
