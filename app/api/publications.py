from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from app.core.database import SessionLocal
from app.models.publication import Publication
from app.schemas.publication import (
    PublicationCreate,
    PublicationResponse,
)


router = APIRouter(
    prefix="/publications",
    tags=["Publications"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("", response_model=PublicationResponse)
def create_publication(
    data: PublicationCreate,
    db: Session = Depends(get_db),
):
    publication = Publication(
        name=data.name,
        publication_url=data.publication_url,
        rss_url=data.rss_url,
        genre=data.genre,
        source_type=data.source_type,
    )

    db.add(publication)

    try:
        db.commit()
        db.refresh(publication)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Publication already exists.",
        )

    return publication


@router.get("", response_model=list[PublicationResponse])
def get_publications(
    genre: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Publication)

    if genre:
        query = query.filter(
            Publication.genre == genre,
        )

    return query.all()
