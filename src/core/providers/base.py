from abc import ABC, abstractmethod


class BaseBrowserProvider(ABC):

    @abstractmethod
    def start(self, profile_id: str) -> str: ...

    @abstractmethod
    def stop(self, profile_id: str) -> None: ...
