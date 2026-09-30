from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.recommendation import Recommendation
from app.schemas.article import Article


class CandidateFilter:

    def filter(
        self,
        articles: list[Article],
        db: Session,
        max_age_days: int = 30,
        max_candidates: int = 20,
    ) -> list[Article]:

        cutoff = datetime.now(timezone.utc) - timedelta(days=max_age_days)

        recommended_urls = {
            row[0] for row in db.query(Recommendation.article_url).all()
        }

        seen_urls: set[str] = set()
        candidates: list[Article] = []

        for article in articles:

            # Invalid article
            if not article.title or not article.url:
                continue

            # Duplicate in current RSS collection
            if article.url in seen_urls:
                continue

            seen_urls.add(article.url)

            # Already recommended
            if article.url in recommended_urls:
                continue

            # Too old
            if article.published_at:
                published_at = article.published_at

                if published_at.tzinfo is None:
                    published_at = published_at.replace(tzinfo=timezone.utc)

                if published_at < cutoff:
                    continue

            candidates.append(article)

        candidates.sort(
            key=lambda article: (
                article.published_at or datetime.min.replace(tzinfo=timezone.utc)
            ),
            reverse=True,
        )

        return candidates[:max_candidates]
