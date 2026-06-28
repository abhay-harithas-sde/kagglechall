"""
gen_submission.py — generic submission generator
Usage: python gen_submission.py <version_number>
e.g.:  python gen_submission.py 14
"""
import csv, json, sys
from pathlib import Path
from cryptography.fernet import Fernet
import importlib

version = sys.argv[1] if len(sys.argv) > 1 else "14"
mod = importlib.import_module(f"canonical_answers_v{version}")
ANSWERS = mod.ANSWERS

fernet = Fernet(b'6Q_EBPtBG-60URcrF6jxNTJSRjy-CtZbJlvp_xf0c_M=')
SU = 'https://zyro-hr-appdesk-4wmdse8pom22pxvodvzb4w.streamlit.app/'
LU = 'https://smith.langchain.com/public/9e3d2fda-0fec-4640-b410-4eff8b846522/r'

# Load question texts from v12 (stable decrypted set)
v12 = json.loads(Path('answers_v12.json').read_text())
questions = {r['question_id']: r['question'] for r in v12}
QIDs = ['Q01','Q02','Q03','Q04','Q05','Q06','Q07','Q08','Q09','Q10','Q11','Q12','Q13','Q14','Q15']

rows = [{
    'question_id': q,
    'question_enc': fernet.encrypt(questions[q].encode()).decode(),
    'answer_enc': fernet.encrypt(ANSWERS[q].encode()).decode(),
    'streamlit_link': SU,
    'langsmith_link': LU,
} for q in QIDs]

with open('submission.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['question_id','question_enc','answer_enc','streamlit_link','langsmith_link'])
    w.writeheader()
    w.writerows(rows)

out = json.dumps(
    [{'question_id': q, 'question': questions[q], 'answer': ANSWERS[q]} for q in QIDs],
    indent=2, ensure_ascii=False
)
Path(f'answers_v{version}.json').write_text(out)
print(f'v{version}: submission.csv + answers_v{version}.json written ({len(rows)} rows)')
for q in QIDs:
    print(f'  {q}: {ANSWERS[q][:80].replace(chr(10), " | ")}')
