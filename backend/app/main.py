from datetime import datetime, timezone

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import auth as auth_router

Base.metadata.create_all(bind=engine)  # 建立資料表

app = FastAPI(
    title="Doc Assistant API",
    version="0.2.0",
)

app.include_router(auth_router.router)


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "doc-assistant-backend",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
