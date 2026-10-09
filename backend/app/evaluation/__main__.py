import json
from collections import Counter
from app.services.triage import triage_ticket

DATA_FILE = "app/evaluation/test_tickets.json"

def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        cases = json.load(f)

    category_correct = 0
    escalation_correct = 0
    category_counts = Counter()

    for case in cases:
        result = triage_ticket(case["text"])
        if result["category"] == case["expected_category"]:
            category_correct += 1
        if bool(result["escalate"]) == bool(case["expected_escalation"]):
            escalation_correct += 1
        category_counts[case["expected_category"]] += 1

    n = len(cases)
    print("\\n=== Support AI Evaluation ===")
    print(f"Test cases: {n}")
    print(f"Category accuracy: {category_correct / n:.1%}")
    print(f"Escalation accuracy: {escalation_correct / n:.1%}")
    print("\\nExpected category distribution:")
    for k, v in category_counts.items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
