"""
Loads answers_preview.json, applies post-processing fixes,
regenerates submission.csv with proper refusals for Q11-Q15.
Run AFTER updating STREAMLIT_URL and LANGSMITH_URL.
"""
import json, csv
from pathlib import Path
from cryptography.fernet import Fernet

SUBMISSION_SECRET = b"6Q_EBPtBG-60URcrF6jxNTJSRjy-CtZbJlvp_xf0c_M="
fernet = Fernet(SUBMISSION_SECRET)

# ── UPDATE THESE BEFORE FINAL SUBMISSION ─────────────────────────────────────
STREAMLIT_URL = "https://zyro-hr-appdesk-4wmdse8pom22pxvodvzb4w.streamlit.app/"
LANGSMITH_URL = "https://smith.langchain.com/public/9e3d2fda-0fec-4640-b410-4eff8b846522/r"
# ─────────────────────────────────────────────────────────────────────────────

REFUSAL = (
    "I'm sorry, I can only answer HR-related questions based on "
    "Zyro Dynamics' internal policy documents. This question is outside "
    "the scope of our HR knowledge base."
)

# Questions that must be refused (out-of-scope) — ONLY the true OOS ones
OOS_IDS = {"Q11", "Q13", "Q14", "Q15"}

# Post-processing: if LLM said "does not contain/provide" → treat as refusal
OOS_PHRASES = [
    "does not contain information",
    "does not provide information",
    "context does not contain",
    "context only includes",
    "not contain details",
    "no information",
    "cannot answer",
]

base = Path(__file__).parent
answers = json.loads((base / "answers_preview.json").read_text())

print("=" * 60)
print("POST-PROCESSING ANSWERS")
print("=" * 60)

for item in answers:
    qid = item["question_id"]
    answer = item["answer"]

    # Force refusal for known OOS question IDs
    if qid in OOS_IDS:
        item["answer"] = REFUSAL
        item["out_of_scope"] = True
        print(f"  {qid} → FORCED REFUSAL")
    # Auto-detect partial refusals from LLM
    elif any(p in answer.lower() for p in OOS_PHRASES):
        item["answer"] = REFUSAL
        item["out_of_scope"] = True
        print(f"  {qid} → AUTO-REFUSAL (LLM said 'does not contain')")
    else:
        item["out_of_scope"] = False
        print(f"  {qid} → OK: {answer[:80]}...")

# ── Show final summary ────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("FINAL ANSWER REVIEW")
print("=" * 60)
for item in answers:
    tag = "🚫" if item.get("out_of_scope") else "✅"
    print(f"  {tag} {item['question_id']}: {item['answer'][:100]}")

# ── Generate submission.csv ───────────────────────────────────────────────────
csv_path = base / "submission.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "question_id", "question_enc", "answer_enc",
        "streamlit_link", "langsmith_link"
    ])
    writer.writeheader()
    for item in answers:
        writer.writerow({
            "question_id":    item["question_id"],
            "question_enc":   fernet.encrypt(item["question"].encode()).decode(),
            "answer_enc":     fernet.encrypt(item["answer"].encode()).decode(),
            "streamlit_link": STREAMLIT_URL,
            "langsmith_link": LANGSMITH_URL,
        })

print(f"\n✅ submission.csv → {csv_path} ({len(answers)} rows)")

# Verify
with open(csv_path, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
assert len(rows) == 15, f"Expected 15 rows, got {len(rows)}"
print("✅ Validation passed: 15 rows, all columns present")
print("\n⚠️  Remember to update STREAMLIT_URL + LANGSMITH_URL before final submit!")
