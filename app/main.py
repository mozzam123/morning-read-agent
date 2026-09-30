from fastapi import FastAPI

from app.core.database import Base, engine
from app import models

from app.api.preferences import router as preferences_router
from app.api.publications import router as publications_router
from app.api.articles import router as articles_router
from app.api.recommendations import router as recommendations_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Daily Read Agent",
    version="0.1.0",
)

app.include_router(preferences_router)
app.include_router(publications_router)
app.include_router(articles_router)
app.include_router(recommendations_router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "daily-read-agent",
    }
