from sqlalchemy.orm import Session

from app.models.publication import Publication
from app.schemas.article import Article
from app.sources.factory import get_content_source


class ArticleCollector:

    def collect_for_genre(
        self,
        genre: str,
        db: Session,
    ) -> list[Article]:

        publications = (
            db.query(Publication)
            .filter(
                Publication.genre == genre,
                Publication.active.is_(True),
            )
            .all()
        )

        articles: list[Article] = []

        for publication in publications:
            source = get_content_source(publication.source_type)

            publication_articles = source.get_articles(
                rss_url=publication.rss_url,
                publication_name=publication.name,
            )

            articles.extend(publication_articles)

        return articles
