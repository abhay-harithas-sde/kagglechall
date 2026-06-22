import subprocess
import sys

# First, try to install pdfplumber if not present
subprocess.run([
    r"C:\Users\abhay\AppData\Local\Programs\Python\Python313\python.exe",
    "-m", "pip", "install", "pdfplumber", "--quiet"
], capture_output=True)

import importlib
try:
    import pdfplumber
except ImportError:
    print("pdfplumber not available, trying pypdf")
    subprocess.run([
        r"C:\Users\abhay\AppData\Local\Programs\Python\Python313\python.exe",
        "-m", "pip", "install", "pypdf", "--quiet"
    ], capture_output=True)

import pdfplumber

PDF_DIR = r"d:\HACKATHONS AND BUILDATHONS\KAGGLE MASTERCLASS\niat-masterclass-rag-challenge\zyro-dynamics-hr-corpus"

def extract_all_pages(pdf_path):
    """Extract text from all pages of a PDF, returning list of (page_num, text)"""
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            pages.append((i + 1, text))
    return pages

def print_full_pdf(pdf_path, label):
    print(f"\n{'='*80}")
    print(f"FULL TEXT: {label}")
    print(f"{'='*80}")
    pages = extract_all_pages(pdf_path)
    for page_num, text in pages:
        print(f"\n--- PAGE {page_num} ---")
        print(text)

# ============================================================
# 1. 02_Leave_Policy.pdf — ALL pages (to get every section)
# ============================================================
print_full_pdf(
    f"{PDF_DIR}\\02_Leave_Policy.pdf",
    "02_Leave_Policy.pdf — COMPLETE DOCUMENT"
)

# ============================================================
# 2. 03_Work_From_Home_Policy.pdf — ALL pages
# ============================================================
print_full_pdf(
    f"{PDF_DIR}\\03_Work_From_Home_Policy.pdf",
    "03_Work_From_Home_Policy.pdf — COMPLETE DOCUMENT"
)

# ============================================================
# 3. 06_Compensation_and_Benefits_Policy.pdf — ALL pages
# ============================================================
print_full_pdf(
    f"{PDF_DIR}\\06_Compensation_and_Benefits_Policy.pdf",
    "06_Compensation_and_Benefits_Policy.pdf — COMPLETE DOCUMENT"
)

# ============================================================
# 4. 05_Performance_Review_Policy.pdf — ALL pages
# ============================================================
print_full_pdf(
    f"{PDF_DIR}\\05_Performance_Review_Policy.pdf",
    "05_Performance_Review_Policy.pdf — COMPLETE DOCUMENT"
)

print("\n\n" + "="*80)
print("EXTRACTION COMPLETE")
print("="*80)
