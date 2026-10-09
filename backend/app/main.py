from fastapi import FastAPI
from  fastapi.middleware.cors import CORSMiddleware


from app.api.tickets import router as tickets_router
from app.api.analytics import router as analytics_router

app = FastAPI(
    title="Support AI Copilot",
    version="1.0.0",
    description="AI support-ticket triage and grounded response generation."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://support-ticket-triage-agent-fronten.vercel.app",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "service": "support-ai-copilot"}

app.include_router(tickets_router)
app.include_router(analytics_router)
