"""
Kaggle submission script using Bearer token (KGAT_ format).
Usage:  py kaggle_submit.py
"""
import os
import requests
from pathlib import Path

KAGGLE_TOKEN    = "KGAT_ec4e1a08f5581770692d516e0766c9c1"
KAGGLE_USERNAME = "n25h01a0738"
COMPETITION     = "niat-masterclass-rag-challenge"
CSV_PATH        = Path(__file__).parent / "submission.csv"
MESSAGE         = "Zyro Dynamics HR RAG - LLaMA3.3-70B + FAISS + MMR + Guardrails"

HEADERS = {"Authorization": f"Bearer {KAGGLE_TOKEN}"}
BASE    = "https://www.kaggle.com/api/v1"

def submit():
    if not CSV_PATH.exists():
        print(f"❌ submission.csv not found at {CSV_PATH}")
        return

    print(f"📤 Submitting {CSV_PATH.name} to '{COMPETITION}'...")

    # Step 1 — request upload URL
    r = requests.post(
        f"{BASE}/competitions/{COMPETITION}/submissions/url/{CSV_PATH.stat().st_size}",
        headers=HEADERS,
        json={"fileName": CSV_PATH.name},
    )
    print(f"   Upload URL status : {r.status_code}")
    if r.status_code not in (200, 201):
        print("   Response:", r.text[:300])
        return

    data        = r.json()
    upload_url  = data.get("createUrl") or data.get("url")
    submit_token = data.get("token")

    # Step 2 — upload the file
    with open(CSV_PATH, "rb") as f:
        up = requests.put(upload_url, data=f, headers={"Content-Type": "text/csv"})
    print(f"   File upload status: {up.status_code}")

    # Step 3 — finalise submission
    r2 = requests.post(
        f"{BASE}/competitions/submissions/submit/{submit_token}",
        headers=HEADERS,
        json={
            "competitionName": COMPETITION,
            "submissionDescription": MESSAGE,
        },
    )
    print(f"   Submit status     : {r2.status_code}")
    if r2.status_code in (200, 201):
        print("✅ Submission successful!")
        print("   View at: https://www.kaggle.com/competitions/" + COMPETITION + "/submissions")
    else:
        print("   Response:", r2.text[:400])

if __name__ == "__main__":
    submit()
