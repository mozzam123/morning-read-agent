from app.llm.provider import get_llm
from app.schemas.article import Article
from app.schemas.ranking import RankingDecision


class ArticleRanker:

    def __init__(self):
        llm = get_llm()

        self.structured_llm = llm.with_structured_output(RankingDecision)

    def rank(
        self,
        genre: str,
        candidates: list[Article],
    ) -> RankingDecision:

        if not candidates:
            raise ValueError("No candidates available for ranking.")

        candidate_text = self._format_candidates(candidates)

        prompt = f"""
You are selecting ONE article for a personalized daily reading recommendation.

Today's topic:
{genre}

Evaluate the candidate articles based on:

1. Relevance to the topic
2. Practical usefulness
3. Technical depth when appropriate
4. Likely learning value
5. Freshness

Prefer useful, substantive articles over promotional or shallow content.

Candidates:

{candidate_text}

Select exactly one article.

The selected_index must correspond to the candidate index.

Keep the reason concise, approximately 1-2 sentences.
"""

        return self.structured_llm.invoke(prompt)

    def _format_candidates(
        self,
        candidates: list[Article],
    ) -> str:

        formatted = []

        for index, article in enumerate(candidates):
            summary = article.summary or "No summary available."

            formatted.append(
                f"""
INDEX: {index}
TITLE: {article.title}
PUBLICATION: {article.publication}
PUBLISHED: {article.published_at}
SUMMARY:
{summary[:1000]}
"""
            )

        return "\n".join(formatted)
