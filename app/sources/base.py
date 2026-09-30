from abc import ABC, abstractmethod

from app.schemas.article import Article


class ContentSource(ABC):

    @abstractmethod
    def get_articles(
        self,
        rss_url: str,
        publication_name: str,
    ) -> list[Article]:
        pass
