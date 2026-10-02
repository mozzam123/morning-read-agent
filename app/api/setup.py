from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.services.publication_setup import (
    PublicationSetupService,
)


router = APIRouter(
    prefix="/setup",
    tags=["Setup"],
)

service = PublicationSetupService()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/publications")
def setup_publications(
    db: Session = Depends(get_db),
):
    return service.setup(db)
