from abc import ABC, abstractmethod

from src.platforms.instagram.reels.schemas import Reel


class BaseReelStorage(ABC):

    @abstractmethod
    def get_all_reels(self) -> list[Reel]:
        pass

    @abstractmethod
    def save_reels(self, reels: list[Reel]):
        pass
