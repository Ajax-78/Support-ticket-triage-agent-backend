import re

CATEGORY_KEYWORDS = {
    "refund": ["refund", "money back", "paise wapas", "रिफंड"],
    "payment": ["payment", "paid", "deduct", "transaction", "upi", "payment pending", "पैमेंट"],
    "batch_access": ["batch", "course access", "access nahi", "not accessible", "enrollment", "बैच"],
    "technical": ["video", "buffer", "crash", "bug", "login issue", "app", "website", "play nahi", "technical"],
    "academic": ["question", "doubt", "answer", "assignment", "faculty", "teacher", "academic"],
    "account": ["password", "otp", "account", "login", "email change"],
}

def detect_category(text: str):
    t = text.lower()
    scores = {category: 0 for category in CATEGORY_KEYWORDS}

    for category, words in CATEGORY_KEYWORDS.items():
        for word in words:
            if word in t:
                scores[category] += 1

    category = max(scores, key=scores.get)
    if scores[category] == 0:
        return "other", 0.55

    confidence = min(0.96, 0.72 + scores[category] * 0.08)
    return category, confidence

def detect_sentiment(text: str):
    t = text.lower()
    angry = [
        "ridiculous", "worst", "useless", "nobody", "fraud", "scam",
        "cheated", "very angry", "third time", "not responding"
    ]
    frustrated = [
        "please help", "still not", "problem", "issue", "can't", "cannot",
        "nahi ho raha", "nahi mil raha", "not working"
    ]

    if any(x in t for x in angry):
        return "angry"
    if any(x in t for x in frustrated):
        return "frustrated"
    return "neutral"

def detect_issues(text: str, category: str):
    t = text.lower()
    issues = [category]

    if any(x in t for x in ["payment", "paid", "deduct", "upi", "transaction"]):
        if "payment" not in issues:
            issues.append("payment")

    if any(x in t for x in ["access", "course", "batch", "enrollment"]):
        if "access" not in issues:
            issues.append("access")

    if any(x in t for x in ["video", "app", "crash", "bug", "buffer"]):
        if "technical" not in issues:
            issues.append("technical")

    return issues

def make_reply(category: str, sentiment: str):
    replies = {
        "payment": "Hi, we understand that you are facing a payment-related issue. We will verify the transaction and enrollment status and help resolve the access issue.",
        "refund": "Hi, we can help with your refund request. We first need to verify the order and applicable refund policy before confirming eligibility.",
        "batch_access": "Hi, we understand that your batch is not visible. Please verify that you are logged into the account used for enrollment. We can escalate this for an access check if the issue continues.",
        "technical": "Hi, sorry you are facing a technical issue. Please try updating the app or browser, clearing the cache and retrying. If the issue continues, we can escalate it with your device details.",
        "academic": "Hi, we can route your academic question to the appropriate academic support channel. Please share the course and question details if they are not already included.",
        "account": "Hi, we can help with your account access issue. Please use the account recovery process. Never share your password or OTP with support.",
        "other": "Hi, thanks for reaching out. We need a little more information to identify the right support team for your request.",
    }
    return replies.get(category, replies["other"])

def mock_triage(ticket_text: str, evidence: list):
    category, confidence = detect_category(ticket_text)
    sentiment = detect_sentiment(ticket_text)
    issues = detect_issues(ticket_text, category)

    priority = "high" if sentiment == "angry" else "medium" if confidence < 0.8 else "low"

    evidence_out = [
        {
            "source": e["source"],
            "section": e["section"],
            "quote": e["text"],
        }
        for e in evidence
    ]

    return {
        "category": category,
        "confidence": confidence,
        "priority": priority,
        "sentiment": sentiment,
        "issues": issues,
        "escalate": False,
        "escalation_reason": None,
        "draft_reply": make_reply(category, sentiment),
        "evidence": evidence_out,
        "model": "mock-rule-engine",
    }
