from sqlalchemy.orm import Session

from app.schemas.article import Article
from app.services.article_collector import ArticleCollector
from app.services.candidate_filter import CandidateFilter


class CandidateService:

    def __init__(self):
        self.collector = ArticleCollector()
        self.filter = CandidateFilter()

    def get_candidates(
        self,
        genre: str,
        db: Session,
    ) -> list[Article]:

        articles = self.collector.collect_for_genre(
            genre=genre,
            db=db,
        )

        candidates = self.filter.filter(
            articles=articles,
            db=db,
        )

        return candidates
