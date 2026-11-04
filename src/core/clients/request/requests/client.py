import logging
from typing import Optional

import requests
from requests import Session

from src.core.clients.base import BaseRequestClient
from src.core.clients.schemas import RequestDTO, ResponseDTO
from src.core.providers.base import BaseBrowserProvider

logger = logging.getLogger(__name__)


class RequestsClient(BaseRequestClient):
    def __init__(
        self,
        proxy: str | None = None,
        provider: BaseBrowserProvider | None = None,
    ) -> None:
        self._proxy = proxy
        self._provider = provider
        self._session: Optional[Session] = None

    def start(self):
        self._session = requests.Session()
        logger.info("Requests session successfully started")

    def close(self):
        if self._session:
            self._session.close()
        logger.info("Requests session successfully stopped")

    def fetch(self, request_dto: RequestDTO) -> ResponseDTO:
        if not self._session:
            raise RuntimeError("Session not started")

        response = self._session.request(
            method=request_dto.method,
            url=request_dto.url,
            headers=request_dto.headers,
            params=request_dto.params,
            json=request_dto.json,
            data=request_dto.data,
            cookies=request_dto.cookies,
            proxies={"http": self._proxy, "https": self._proxy} if self._proxy else None,
            timeout=request_dto.timeout,
            verify=request_dto.verify,
        )

        response.raise_for_status()

        return ResponseDTO(
            url=response.url,
            status=response.status_code,
            request_info={
                "method": response.request.method,
                "headers": dict(response.request.headers),
                "body": response.request.body,
            },
            response=response.content,
        )
