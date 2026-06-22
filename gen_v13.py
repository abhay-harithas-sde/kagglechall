import csv, json
from pathlib import Path
from cryptography.fernet import Fernet
from canonical_answers_v13 import ANSWERS

fernet = Fernet(b'6Q_EBPtBG-60URcrF6jxNTJSRjy-CtZbJlvp_xf0c_M=')
SU = 'https://zyro-hr-appdesk-4wmdse8pom22pxvodvzb4w.streamlit.app/'
LU = 'https://smith.langchain.com/public/9e3d2fda-0fec-4640-b410-4eff8b846522/r'

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

Path('answers_v13.json').write_text(json.dumps(
    [{'question_id': q, 'question': questions[q], 'answer': ANSWERS[q]} for q in QIDs],
    indent=2, ensure_ascii=False
))
print(f'Done - {len(rows)} rows written to submission.csv')
for q in QIDs:
    print(f'  {q}: {ANSWERS[q][:90].replace(chr(10), " | ")}')
