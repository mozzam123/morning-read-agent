from datetime import datetime

import feedparser

from app.schemas.article import Article
from app.sources.base import ContentSource


class SubstackSource(ContentSource):

    def get_articles(
        self,
        rss_url: str,
        publication_name: str,
    ) -> list[Article]:

        feed = feedparser.parse(rss_url)

        if feed.bozo and not feed.entries:
            raise ValueError(f"Invalid RSS feed: {rss_url}")

        articles = []

        for entry in feed.entries:
            published_at = None

            if getattr(entry, "published_parsed", None):
                published_at = datetime(*entry.published_parsed[:6])

            article = Article(
                title=entry.get("title", ""),
                url=entry.get("link", ""),
                publication=publication_name,
                published_at=published_at,
                summary=entry.get("summary"),
            )

            articles.append(article)

        return articles
