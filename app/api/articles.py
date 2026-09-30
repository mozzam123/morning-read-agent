from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.schemas.article import Article
from app.services.article_collector import ArticleCollector
from app.services.candidate_service import CandidateService


router = APIRouter(
    prefix="/articles",
    tags=["Articles"],
)

collector = ArticleCollector()
candidate_service = CandidateService()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/collect/{genre}", response_model=list[Article])
def collect_articles(
    genre: str,
    db: Session = Depends(get_db),
):
    return collector.collect_for_genre(
        genre=genre,
        db=db,
    )


@router.get("/candidates/{genre}", response_model=list[Article])
def get_candidates(
    genre: str,
    db: Session = Depends(get_db),
):
    return candidate_service.get_candidates(
        genre=genre,
        db=db,
    )
