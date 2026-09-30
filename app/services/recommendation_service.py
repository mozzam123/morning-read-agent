from sqlalchemy.orm import Session

from app.schemas.ranking import RankedArticle
from app.services.article_ranker import ArticleRanker
from app.services.candidate_service import CandidateService


class RecommendationService:

    def __init__(self):
        self.candidate_service = CandidateService()
        self.ranker = ArticleRanker()

    def recommend(
        self,
        genre: str,
        db: Session,
    ) -> RankedArticle:

        candidates = self.candidate_service.get_candidates(
            genre=genre,
            db=db,
        )

        if not candidates:
            raise ValueError(f"No candidates available for genre: {genre}")

        decision = self.ranker.rank(
            genre=genre,
            candidates=candidates,
        )

        if not 0 <= decision.selected_index < len(candidates):
            raise ValueError("LLM returned an invalid candidate index.")

        selected_article = candidates[decision.selected_index]

        return RankedArticle(
            article=selected_article,
            reason=decision.reason,
        )
