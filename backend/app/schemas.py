from typing import List, Literal, Optional
from pydantic import BaseModel, Field

Category = Literal[
    "refund",
    "payment",
    "batch_access",
    "technical",
    "academic",
    "account",
    "other",
]

class TicketCreate(BaseModel):
    text: str = Field(min_length=3, max_length=5000)

class Evidence(BaseModel):
    source: str
    section: str
    quote: str

class TriageResult(BaseModel):
    category: Category
    confidence: float = Field(ge=0, le=1)
    priority: Literal["low", "medium", "high"]
    sentiment: Literal["neutral", "positive", "frustrated", "angry"]
    issues: List[str]
    escalate: bool
    escalation_reason: Optional[str] = None
    draft_reply: str
    evidence: List[Evidence]
    model: str
    latency_ms: int
