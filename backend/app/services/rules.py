from app.config import CONFIDENCE_THRESHOLD

HIGH_RISK_WORDS = [
    "lawyer", "legal", "police", "fraud", "scam", "consumer court",
    "chargeback", "cheated", "cheating", "threat", "complaint"
]

def apply_escalation_rules(result: dict, ticket_text: str) -> dict:
    reasons = []

    if result["confidence"] < CONFIDENCE_THRESHOLD:
        reasons.append(
            f"AI confidence {result['confidence']:.0%} is below "
            f"the {CONFIDENCE_THRESHOLD:.0%} auto-resolution threshold."
        )

    if result["category"] == "refund":
        reasons.append("Refund requests require policy/order verification.")

    if "payment" in result["issues"] and "access" in result["issues"]:
        reasons.append("Payment/access mismatch requires account verification.")

    if result["sentiment"] == "angry":
        reasons.append("Highly frustrated student should receive human attention.")

    lowered = ticket_text.lower()
    matched = [w for w in HIGH_RISK_WORDS if w in lowered]
    if matched:
        reasons.append("High-risk language detected: " + ", ".join(matched))

    if not result["evidence"]:
        reasons.append("No sufficiently relevant knowledge-base evidence was found.")

    result["escalate"] = bool(reasons)
    result["escalation_reason"] = " ".join(reasons) if reasons else None

    if result["escalate"] and result["priority"] == "low":
        result["priority"] = "medium"

    return result
