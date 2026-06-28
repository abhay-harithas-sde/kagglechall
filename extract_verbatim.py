import pdfplumber, sys
from pathlib import Path

BASE = Path(r"d:\HACKATHONS AND BUILDATHONS\KAGGLE MASTERCLASS\niat-masterclass-rag-challenge\zyro-dynamics-hr-corpus")

files = {
    "LEAVE":   "02_Leave_Policy.pdf",
    "COMP":    "06_Compensation_and_Benefits_Policy.pdf",
    "PERF":    "05_Performance_Review_Policy.pdf",
    "WFH":     "03_Work_From_Home_Policy.pdf",
    "ONBOARD": "09_Onboarding_and_Separation_Policy.pdf",
    "TRAVEL":  "10_Travel_and_Expense_Policy.pdf",
    "CONDUCT": "04_Code_of_Conduct.pdf",
    "HANDBOOK":"01_Employee_Handbook.pdf",
}

target = sys.argv[1] if len(sys.argv) > 1 else "ALL"

for key, fname in files.items():
    if target != "ALL" and target != key:
        continue
    print(f"\n{'='*70}")
    print(f"FILE: {fname}")
    print('='*70)
    with pdfplumber.open(BASE / fname) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                print(f"\n--- Page {i+1} ---")
                print(text)
