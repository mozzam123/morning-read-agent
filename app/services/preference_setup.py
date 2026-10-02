from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.preference import Preference


class PreferenceSetupService:

    def sync(self, db: Session) -> list[str]:
        interests = settings.get_interests()

        existing_preferences = db.query(Preference).all()

        existing_by_genre = {
            preference.genre: preference for preference in existing_preferences
        }

        configured_interests = set(interests)

        # Add newly configured interests.
        for interest in interests:
            if interest not in existing_by_genre:
                db.add(
                    Preference(
                        genre=interest,
                    )
                )

        # Remove interests no longer configured.
        for preference in existing_preferences:
            if preference.genre not in configured_interests:
                db.delete(preference)

        db.commit()

        return interests
