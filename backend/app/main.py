from fastapi import FastAPI
from datetime import datetime, timezone

app = FastAPI(
    title="Doc Assistant API",
    version="0.1.0",
)


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "doc-assistant-backend",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
