import logging

from app.core.database import SessionLocal
from app.delivery.email import EmailDelivery
from app.services.genre_selector import GenreSelector
from app.services.recommendation_history import RecommendationHistory
from app.services.recommendation_service import RecommendationService


logger = logging.getLogger(__name__)

genre_selector = GenreSelector()
recommendation_service = RecommendationService()
recommendation_history = RecommendationHistory()
delivery = EmailDelivery()


def run_daily_read():

    db = SessionLocal()

    try:
        genre = genre_selector.select(db)

        logger.info(
            "Selected daily genre: %s",
            genre,
        )

        result = recommendation_service.recommend(
            genre=genre,
            db=db,
        )

        if result.get("error"):
            logger.error(
                "Daily recommendation failed: %s",
                result["error"],
            )
            return

        article = result["selected_article"]

        # Deliver first.
        delivery.send(
            genre=genre,
            article=article,
            reason=result["reason"],
        )

        # Only successful deliveries enter recommendation history.
        recommendation_history.save(
            genre=genre,
            article=article,
            db=db,
        )

        logger.info(
            "Daily Read delivered successfully: %s",
            article.title,
        )

    except Exception:
        logger.exception("Daily Read job failed.")

    finally:
        db.close()
