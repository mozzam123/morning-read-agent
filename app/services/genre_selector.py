import random

from sqlalchemy.orm import Session

from app.models.preference import Preference


class GenreSelector:

    def select(
        self,
        db: Session,
    ) -> str:

        preferences = db.query(Preference).all()

        if not preferences:
            raise ValueError("No user preferences configured.")

        selected = random.choice(preferences)

        return selected.genre
