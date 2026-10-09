from fastapi import APIRouter

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/summary")
def summary():
    return {
        "total_tickets": 128,
        "auto_resolved": 91,
        "escalated": 37,
        "accuracy": 91.7,
        "avg_confidence": 89.4,
        "avg_latency_ms": 1850,
        "categories": [
            {"name": "Payment", "count": 36},
            {"name": "Technical", "count": 31},
            {"name": "Batch Access", "count": 24},
            {"name": "Refund", "count": 18},
            {"name": "Academic", "count": 12},
            {"name": "Account", "count": 7},
        ],
    }
