from abc import ABC, abstractmethod

from app.schemas.article import Article


class DeliveryProvider(ABC):

    @abstractmethod
    def send(
        self,
        genre: str,
        article: Article,
        reason: str,
    ) -> None:
        pass
