from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.tts import (
    analysis_router,
    router as tts_router,
    transcription_router,
)
from app.routes.voices import router as voices_router


app = FastAPI(
    title="Text-to-Speech API",
    description="Local offline Text-to-Speech API using Piper",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Text-to-Speech API is running"
    }


@app.get("/api/health")
def health():
    return {
        "status": "ok"
    }


app.include_router(tts_router)
app.include_router(analysis_router)
app.include_router(transcription_router)
app.include_router(voices_router)