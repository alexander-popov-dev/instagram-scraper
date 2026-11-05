import logging
import time

import requests

from src.settings import get_settings

logger = logging.getLogger(__name__)

_TELEGRAM_TIMEOUT = 10
_RATE_LIMIT_RETRIES = 3

settings = get_settings()


class TelegramManager:
    """Sends notifications to a configured Telegram channel."""

    @staticmethod
    def send_message(message: str) -> None:
        """Send a MarkdownV2 message to the Telegram channel; retries on 429, logs errors on failure."""
        if not (settings.telegram_bot_token and settings.telegram_chat_id and settings.telegram_thread_id):
            return

        url = f'https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage'
        payload = {
            'chat_id': settings.telegram_chat_id,
            'message_thread_id': settings.telegram_thread_id,
            'text': message,
            'parse_mode': 'MarkdownV2',
        }

        for attempt in range(_RATE_LIMIT_RETRIES):
            try:
                response = requests.post(url, data=payload, timeout=_TELEGRAM_TIMEOUT)
                if response.status_code == 200:
                    return
                if response.status_code == 429:
                    retry_after = response.json().get('parameters', {}).get('retry_after', 5)
                    logger.warning(f'Telegram rate limit hit, retrying in {retry_after}s')
                    time.sleep(retry_after)
                    continue
                logger.error(f'Telegram send failed: {response.status_code} {response.text}')
                return
            except requests.RequestException as e:
                logger.error(f'Telegram request error: {e}')
                return
