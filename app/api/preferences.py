from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.preference import Preference
from app.schemas.preference import (
    PreferenceCreate,
    PreferenceResponse,
)


router = APIRouter(
    prefix="/preferences",
    tags=["Preferences"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("", response_model=PreferenceResponse)
def create_preference(
    data: PreferenceCreate,
    db: Session = Depends(get_db),
):
    preference = Preference(
        genre=data.genre,
    )

    db.add(preference)
    db.commit()
    db.refresh(preference)

    return preference


@router.get("", response_model=list[PreferenceResponse])
def get_preferences(
    db: Session = Depends(get_db),
):
    return db.query(Preference).all()
