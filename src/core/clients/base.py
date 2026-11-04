from abc import ABC, abstractmethod
from typing import Self

from playwright.sync_api import Page

from src.core.clients.schemas import RequestDTO, ResponseDTO


class BaseClient(ABC):

    @abstractmethod
    async def start(self) -> None: ...

    @abstractmethod
    async def close(self) -> None: ...

    async def __aenter__(self) -> Self:
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()


class BaseRequestClient(BaseClient):

    @abstractmethod
    async def start(self) -> None: ...

    @abstractmethod
    async def close(self) -> None: ...

    @abstractmethod
    async def fetch(self, request_dto: RequestDTO) -> ResponseDTO: ...


class BaseBrowserClient(BaseClient):
    @abstractmethod
    async def start(self) -> None: ...

    @abstractmethod
    async def close(self) -> None: ...

    @abstractmethod
    async def get_page(self) -> Page: ...
