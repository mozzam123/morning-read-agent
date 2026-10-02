from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.services.recommendation_service import RecommendationService


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)

service = RecommendationService()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/generate/{genre}")
def generate_recommendation(
    genre: str,
    db: Session = Depends(get_db),
):
    result = service.recommend(
        genre=genre,
        db=db,
    )

    if result.get("error"):
        raise HTTPException(
            status_code=400,
            detail=result["error"],
        )

    return {
        "genre": genre,
        "article": result["selected_article"],
        "reason": result["reason"],
    }
