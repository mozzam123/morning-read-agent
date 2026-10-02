from fastapi import FastAPI

from app.core.database import Base, engine
from app import models

from app.api.publications import router as publications_router
from app.api.articles import router as articles_router
from app.api.recommendations import router as recommendations_router
from app.api.setup import router as setup_router
from contextlib import asynccontextmanager
from app.core.database import SessionLocal
from app.services.preference_setup import PreferenceSetupService
from app.services.publication_setup import PublicationSetupService

from app.scheduler import start_scheduler, scheduler

Base.metadata.create_all(bind=engine)

preference_setup = PreferenceSetupService()
publication_setup = PublicationSetupService()


@asynccontextmanager
async def lifespan(app: FastAPI):

    db = SessionLocal()
    try:
        preference_setup.sync(db)
        publication_setup.setup(db)

    finally:
        db.close()
    start_scheduler()
    yield
    if scheduler.running:
        scheduler.shutdown()


app = FastAPI(
    title="Daily Read Agent",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(publications_router)
app.include_router(articles_router)
app.include_router(recommendations_router)
app.include_router(setup_router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "daily-read-agent",
    }
