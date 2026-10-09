import time
from app.config import MOCK_AI
from app.schemas import TriageResult
from app.services.retriever import KBRetriever
from app.services.rules import apply_escalation_rules
from app.services.mock_ai import mock_triage
from app.services.claude import claude_triage

retriever = KBRetriever()

def triage_ticket(ticket_text: str) -> dict:
    started = time.perf_counter()

    evidence = retriever.search(ticket_text, top_k=3)

    if MOCK_AI:
        result = mock_triage(ticket_text, evidence)
    else:
        result = claude_triage(ticket_text, evidence)

    result = apply_escalation_rules(result, ticket_text)

    result["latency_ms"] = int((time.perf_counter() - started) * 1000)
    TriageResult(**result)
    return result
