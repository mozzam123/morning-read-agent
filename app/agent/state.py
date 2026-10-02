from typing import TypedDict

from app.schemas.article import Article


class RecommendationState(TypedDict, total=False):
    genre: str

    candidates: list[Article]

    selected_article: Article

    reason: str

    error: str
