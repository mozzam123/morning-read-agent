import random

from sqlalchemy.orm import Session

from app.models.preference import Preference
from app.models.publication import Publication


class GenreSelector:

    def select(
        self,
        db: Session,
    ) -> str:

        available_genres = (
            db.query(Preference.genre)
            .join(
                Publication,
                Publication.genre == Preference.genre,
            )
            .filter(
                Publication.active.is_(True),
            )
            .distinct()
            .all()
        )

        if not available_genres:
            raise ValueError("No configured genres have active publications.")

        genres = [row[0] for row in available_genres]

        return random.choice(genres)
