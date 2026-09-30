from pydantic import BaseModel, ConfigDict


class PreferenceCreate(BaseModel):
    genre: str


class PreferenceResponse(BaseModel):
    id: int
    genre: str

    model_config = ConfigDict(from_attributes=True)
