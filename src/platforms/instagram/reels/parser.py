import logging

from src.platforms.instagram.reels.schemas import Reel

logger = logging.getLogger(__name__)


class ReelsParser:
    def parse(self, data: dict) -> list[Reel]:
        reels = []

        for reel in data["data"]["xdt_api__v1__clips__home__connection_v2"]["edges"]:
            reel = reel["node"]["media"]
            audio_data = reel["clips_metadata"]["original_sound_info"] or reel["clips_metadata"]["music_info"]
            trending_audio = audio_data.get("consumption_info", {}).get("is_trending_in_clips")
            trending_music = audio_data.get("music_consumption_info", {}).get("is_trending_in_clips")

            logging.info(f'Parsing: {reel["pk"]}')

            reels.append(
                Reel(
                    url=f'https://www.instagram.com/reels/{reel["code"]}',
                    media_code=reel["code"],
                    media_id=reel["pk"],
                    taken_at=reel["taken_at"],
                    author_id=reel["user"]["pk"],
                    author_username=reel["user"]["username"],
                    author_full_name=reel["user"]["full_name"],
                    is_verified=reel["user"]["is_verified"],
                    caption=reel["caption"]["text"].replace("\n", " ") if reel["caption"] else "",
                    like_count=reel["like_count"],
                    comment_count=reel["comment_count"],
                    repost_count=reel["media_repost_count"],
                    video_url=reel["video_versions"][0]["url"],
                    thumbnail_url=reel["image_versions2"]["candidates"][0]["url"],
                    audio_id=audio_data.get("audio_asset_id") or audio_data.get("music_asset_info").get(
                        "audio_cluster_id"),
                    audio_title=audio_data.get("original_audio_title") or audio_data.get("music_asset_info").get(
                        "title"),
                    inventory_source=reel["inventory_source"],
                    is_trending_audio=trending_audio if trending_audio is not None else trending_music,
                )
            )
        return reels
