from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import CORS_ORIGINS
from app.api.tickets import router as tickets_router
from app.api.analytics import router as analytics_router

app = FastAPI(
    title="Support AI Copilot",
    version="1.0.0",
    description="AI support-ticket triage and grounded response generation."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "service": "support-ai-copilot"}

app.include_router(tickets_router)
app.include_router(analytics_router)
