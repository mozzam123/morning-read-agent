from langgraph.graph import END, START, StateGraph
from sqlalchemy.orm import Session

from app.agent.state import RecommendationState
from app.services.article_ranker import ArticleRanker
from app.services.candidate_service import CandidateService


class RecommendationGraph:

    def __init__(self, db: Session):
        self.db = db

        self.candidate_service = CandidateService()
        self.ranker = ArticleRanker()

        self.graph = self._build_graph()

    def _build_graph(self):
        builder = StateGraph(RecommendationState)

        builder.add_node(
            "collect_candidates",
            self.collect_candidates,
        )

        builder.add_node(
            "rank_article",
            self.rank_article,
        )

        builder.add_edge(
            START,
            "collect_candidates",
        )

        builder.add_conditional_edges(
            "collect_candidates",
            self.after_collection,
            {
                "rank": "rank_article",
                "stop": END,
            },
        )

        builder.add_edge(
            "rank_article",
            END,
        )

        return builder.compile()

    def collect_candidates(self, state: RecommendationState):
        genre = state["genre"]

        candidates = self.candidate_service.get_candidates(
            genre=genre,
            db=self.db,
        )

        if not candidates:
            return {
                "candidates": [],
                "error": (f"No candidates available for genre: {genre}"),
            }

        return {
            "candidates": candidates,
        }

    def after_collection(self, state: RecommendationState) -> str:

        if state.get("error"):
            return "stop"

        return "rank"

    def rank_article(
        self,
        state: RecommendationState,
    ):
        candidates = state["candidates"]
        genre = state["genre"]

        try:
            decision = self.ranker.rank(
                genre=genre,
                candidates=candidates,
            )

        except Exception as exc:
            return {"error": (f"Article ranking failed: {str(exc)}")}

        if not 0 <= decision.selected_index < len(candidates):
            return {"error": ("LLM returned an invalid candidate index.")}

        selected_article = candidates[decision.selected_index]

        return {
            "selected_article": selected_article,
            "reason": decision.reason,
        }
