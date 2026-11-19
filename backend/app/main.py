"""HTTP API for simulated NetScope traffic metrics."""

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from app.simulator import current_sample, history_samples

app = FastAPI(title="NetScope API", description="Demo endpoints backed by simulated network traffic data.", version="0.1.0")

app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_credentials=True, allow_methods=["GET"], allow_headers=["*"])


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/traffic/summary")
def traffic_summary() -> dict:
    return current_sample()


@app.get("/api/traffic/history")
def traffic_history(points: int = Query(default=30, ge=2, le=120)) -> dict:
    return {"samples": history_samples(points)}
