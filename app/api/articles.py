from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.schemas.article import Article
from app.services.article_collector import ArticleCollector


router = APIRouter(
    prefix="/articles",
    tags=["Articles"],
)

collector = ArticleCollector()


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
