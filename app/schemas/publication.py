from pydantic import BaseModel, ConfigDict


class PublicationCreate(BaseModel):
    name: str
    publication_url: str
    rss_url: str
    genre: str
    source_type: str = "substack"


class PublicationResponse(BaseModel):
    id: int
    name: str
    publication_url: str
    rss_url: str
    genre: str
    source_type: str
    active: bool

    model_config = ConfigDict(from_attributes=True)
