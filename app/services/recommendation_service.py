from sqlalchemy.orm import Session

from app.agent.graph import RecommendationGraph


class RecommendationService:

    def recommend(
        self,
        genre: str,
        db: Session,
    ):
        workflow = RecommendationGraph(
            db=db,
        )

        result = workflow.graph.invoke(
            {
                "genre": genre,
            }
        )

        return result
