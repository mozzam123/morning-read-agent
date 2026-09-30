from fastapi import FastAPI

from app.core.database import Base, engine
from app import models


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Daily Read Agent",
    version="0.1.0",
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "daily-read-agent",
    }
