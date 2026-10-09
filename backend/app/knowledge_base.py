KNOWLEDGE_BASE = [
    {
        "source": "payment_policy.md",
        "section": "Successful payment but course unavailable",
        "text": (
            "If payment has been successfully completed but course access is unavailable, "
            "support should verify the transaction and enrollment status. If payment is "
            "confirmed but enrollment cannot be restored automatically, escalate to payment operations."
        ),
    },
    {
        "source": "payment_policy.md",
        "section": "Payment pending",
        "text": (
            "For a payment showing pending, ask the student to wait for the payment provider "
            "to update the transaction status. Do not promise an exact settlement time."
        ),
    },
    {
        "source": "refund_policy.md",
        "section": "Refund requests",
        "text": (
            "Refund eligibility depends on the product policy and purchase date. A support "
            "agent should verify the order before confirming eligibility. If the request needs "
            "manual approval, escalate it to the refund team."
        ),
    },
    {
        "source": "batch_access.md",
        "section": "Batch access",
        "text": (
            "If a student cannot see a purchased batch, verify enrollment and account identity. "
            "If enrollment is correct but the batch remains unavailable, escalate to the access team."
        ),
    },
    {
        "source": "technical_support.md",
        "section": "Video playback",
        "text": (
            "For video playback problems, ask the student to check connectivity, update the app "
            "or browser, clear cache, and retry. If the issue persists across devices, escalate "
            "with device and browser details."
        ),
    },
    {
        "source": "technical_support.md",
        "section": "App crash",
        "text": (
            "For repeated app crashes, collect app version, device model and operating system. "
            "A reproducible crash should be escalated to technical support."
        ),
    },
    {
        "source": "academic_support.md",
        "section": "Academic doubts",
        "text": (
            "Academic questions should be routed to the relevant academic support channel. "
            "Support should not invent an answer when the required course material is unavailable."
        ),
    },
    {
        "source": "account_support.md",
        "section": "Account access",
        "text": (
            "For account access problems, verify the registered email or phone number and follow "
            "the account recovery process. Never ask a student to share a password or OTP."
        ),
    },
]

def kb_documents():
    return KNOWLEDGE_BASE
