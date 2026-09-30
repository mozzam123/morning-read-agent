from datetime import datetime

from pydantic import BaseModel


class Article(BaseModel):
    title: str
    url: str
    publication: str
    published_at: datetime | None = None
    summary: str | None = None
