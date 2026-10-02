from sqlalchemy.orm import Session

from app.models.recommendation import Recommendation
from app.schemas.article import Article


class RecommendationHistory:

    def save(
        self,
        genre: str,
        article: Article,
        db: Session,
    ) -> Recommendation:

        recommendation = Recommendation(
            article_url=article.url,
            title=article.title,
            genre=genre,
            publication=article.publication,
        )

        try:
            db.add(recommendation)
            db.commit()
            db.refresh(recommendation)

        except Exception:
            db.rollback()
            raise

        return recommendation
