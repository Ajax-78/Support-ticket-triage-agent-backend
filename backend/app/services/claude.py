import json
import time
from anthropic import Anthropic

from app.config import ANTHROPIC_API_KEY, ANTHROPIC_MODEL
from app.schemas import TriageResult

SYSTEM_PROMPT = """
You are an AI support-ticket triage assistant for an education company.

Your job:
1. Classify the student ticket.
2. Identify all meaningful issues.
3. Detect sentiment.
4. Assign priority.
5. Draft a helpful response.
6. Use ONLY the supplied knowledge-base evidence for policy claims.
7. Never invent refund eligibility, timelines, guarantees, or account actions.
8. If the evidence is insufficient, set escalate=true.
9. Support English, Hindi and Hinglish.
10. Return ONLY valid JSON matching the requested schema.

Allowed categories:
refund, payment, batch_access, technical, academic, account, other.

Output JSON:
{
  "category": "...",
  "confidence": 0.0,
  "priority": "low|medium|high",
  "sentiment": "neutral|positive|frustrated|angry",
  "issues": ["..."],
  "escalate": true,
  "escalation_reason": "...",
  "draft_reply": "...",
  "evidence": [
    {
      "source": "...",
      "section": "...",
      "quote": "..."
    }
  ]
}
"""

def claude_triage(ticket_text: str, evidence: list) -> dict:
    if not ANTHROPIC_API_KEY:
        raise RuntimeError("ANTHROPIC_API_KEY is missing")

    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    evidence_text = "\n\n".join(
        f"SOURCE: {e['source']}\nSECTION: {e['section']}\nCONTENT: {e['text']}"
        for e in evidence
    )

    prompt = f"""
STUDENT TICKET:
{ticket_text}

KNOWLEDGE BASE EVIDENCE:
{evidence_text if evidence_text else "No relevant evidence found."}

Return only JSON.
"""

    started = time.perf_counter()
    response = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=1200,
        temperature=0,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    latency_ms = int((time.perf_counter() - started) * 1000)

    raw = "".join(
        block.text for block in response.content
        if getattr(block, "type", None) == "text"
    ).strip()

    if raw.startswith("```"):
        raw = raw.replace("```json", "").replace("```", "").strip()

    data = json.loads(raw)
    validated = TriageResult(
        category=data["category"],
        confidence=float(data["confidence"]),
        priority=data["priority"],
        sentiment=data["sentiment"],
        issues=data["issues"],
        escalate=bool(data.get("escalate", False)),
        escalation_reason=data.get("escalation_reason"),
        draft_reply=data["draft_reply"],
        evidence=data.get("evidence", []),
        model=ANTHROPIC_MODEL,
        latency_ms=latency_ms,
    )
    return validated.model_dump()
