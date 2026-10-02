import logging

from app.core.database import SessionLocal
from app.services.genre_selector import GenreSelector
from app.services.recommendation_service import RecommendationService


logger = logging.getLogger(__name__)

genre_selector = GenreSelector()
recommendation_service = RecommendationService()


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

        print()
        print("=" * 60)
        print("☀️ TODAY'S READ")
        print("=" * 60)
        print(f"Topic: {genre}")
        print()
        print(article.title)
        print()
        print("Why this was selected:")
        print(result["reason"])
        print()
        print(f"Read: {article.url}")
        print("=" * 60)
        print()

    except Exception:
        logger.exception("Daily Read job failed.")

    finally:
        db.close()
