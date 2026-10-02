from sqlalchemy.orm import Session

from app.models.preference import Preference
from app.models.publication import Publication
from app.sources.factory import get_content_source
from app.sources.registry import CURATED_SOURCES


class PublicationSetupService:

    def setup(self, db: Session) -> dict:

        preferences = db.query(Preference).all()

        added = []
        skipped = []
        unsupported = []

        for preference in preferences:

            sources = CURATED_SOURCES.get(preference.genre)

            if not sources:
                unsupported.append(preference.genre)
                continue

            for source_config in sources:

                existing = (
                    db.query(Publication)
                    .filter(Publication.rss_url == source_config["rss_url"])
                    .first()
                )

                if existing:
                    skipped.append(source_config["name"])
                    continue

                if not self._validate_source(source_config):
                    skipped.append(source_config["name"])
                    continue

                publication = Publication(
                    name=source_config["name"],
                    publication_url=source_config["publication_url"],
                    rss_url=source_config["rss_url"],
                    genre=preference.genre,
                    source_type=source_config["source_type"],
                    active=True,
                )

                db.add(publication)

                added.append(source_config["name"])

        db.commit()

        return {
            "added": added,
            "skipped": skipped,
            "unsupported_interests": unsupported,
        }

    def _validate_source(
        self,
        source_config: dict,
    ) -> bool:

        try:
            source = get_content_source(source_config["source_type"])

            articles = source.get_articles(
                rss_url=source_config["rss_url"],
                publication_name=source_config["name"],
            )

            return len(articles) > 0

        except Exception:
            return False
