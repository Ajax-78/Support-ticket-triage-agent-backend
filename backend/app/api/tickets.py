from fastapi import APIRouter, HTTPException
from app.schemas import TicketCreate
from app.services.triage import triage_ticket

router = APIRouter(prefix="/api/tickets", tags=["tickets"])

@router.post("/triage")
def triage(ticket: TicketCreate):
    try:
        result = triage_ticket(ticket.text)
        return {
            "ticket": ticket.text,
            "result": result
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@router.get("/knowledge-base")
def knowledge_base():
    from app.knowledge_base import kb_documents
    return {"documents": kb_documents()}
