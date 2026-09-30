from pydantic import BaseModel, Field

from app.schemas.article import Article


class RankingDecision(BaseModel):
    selected_index: int = Field(
        description="Index of the best article from the candidate list."
    )

    reason: str = Field(
        description=("A short explanation of why this article is worth reading.")
    )


class RankedArticle(BaseModel):
    article: Article
    reason: str
