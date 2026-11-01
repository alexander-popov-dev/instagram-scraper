from datetime import datetime

from pydantic import BaseModel


class Reel(BaseModel):
    media_code: str                  # code
    media_id: str                   # pk
    taken_at: datetime              # taken_at
    author_id: str                  # user.pk
    author_username: str            # user.username
    author_full_name: str | None    # user.full_name
    is_verified: bool               # user.is_verified
    caption: str | None             # caption.text
    like_count: int | None          # like_count
    comment_count: int | None       # comment_count
    repost_count: int | None        # media_repost_count
    video_url: str | None           # video_versions[0].url
    thumbnail_url: str | None       # image_versions2.candidates[0].url
    audio_id: str | None            # original_sound_info / music_info
    audio_title: str | None         # clips_metadata.original_sound_info.original_audio_title
    is_trending_audio: bool         # clips_metadata.original_sound_info.consumption_info.is_trending_in_clips
    inventory_source: str | None    # inventory_source