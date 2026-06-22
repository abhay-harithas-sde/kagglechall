"""
submit_v10.py — v10: Pure fresh RAG output from run_pipeline.py
Uses answers_preview.json directly — no manual edits.
This style previously scored 93.33 (BM25+FAISS hybrid).
"""
import csv, json, sys
from pathlib import Path
from cryptography.fernet import Fernet

SUBMISSION_SECRET = b"6Q_EBPtBG-60URcrF6jxNTJSRjy-CtZbJlvp_xf0c_M="
fernet = Fernet(SUBMISSION_SECRET)

STREAMLIT_URL = "https://zyro-hr-appdesk-4wmdse8pom22pxvodvzb4w.streamlit.app/"
LANGSMITH_URL = "https://smith.langchain.com/public/9e3d2fda-0fec-4640-b410-4eff8b846522/r"

_Q = [
    ("Q01", "gAAAAABqE-m-EnBhR94RLAsyCD5YUOimCgpyxnGmrg3N29dvcCChh_LbQzGhacqtB6Rg9ySTN-aO4eS5nnSSqgvslxWg3T2XNxvKRw9BoZOGB8sSrPpeXOqPKhdprAkvepa0Ef13rK84Lx_QKNPq5AMeO2zweDFo-UGpOZ1yFV_k0NbpkP0MshR9BpjCI4QpkDSx9QH95aeCK8sqSIkcM8wOFRs1hRD_tV-Jg4XmeHLm4jW6wpCWQRBF-XWIHTwCE3Tod-Zfj-nIFpPe3sNmXFDNY_L5g8aAiw=="),
    ("Q02", "gAAAAABqE-m-iGIUkxaPu-TWqkoQqfrY1QvCn-VC445z8EzeRjBVVSjcBgTYC-OS2QVoM37Oh8tFkJdLJcdivCIg9-jTJ72Vy24BQwagKYrIJlkNBr9yectRVtDZ_X24PWpsbIdMcelH1a6VBz9XXmJ19-0HvqFT0kTeEQEyjzKL2BmtoSHOquqe74xGFhpWD-fI1Cshfxk9EXwgA4poqi7JJ3ovja5pVM18uwfNAmcNacnQRtFTAm6x1JmXKSYVeBSbgpOv1zjEEC-0XfVhF0Wtwli0hRZHhA=="),
    ("Q03", "gAAAAABqE-m-qhjI3OCH68smnD4afuA_GmeOO8rI6R79iaPeodfwbt4NTlWhlbSfgr8BP9ZNAi5yczk65fgsIgbRXQ9AkAVDE2NOD11Aqt6U_NqURkjBQpzn3gzTQNj2qNwtkhx71-l8uYIfZLu8Z-Nv4aAkEaFTKCDp4DWgCaFJbe90TCA2fGUVnDiaI1_0ID87AHR-yYRwTaKYiWI7PiCQWFVm22NGx3cwX_uvMouAEXLX2sw_o3s="),
    ("Q04", "gAAAAABqE-m-qVKLekYizIYVBejJAmZYhT0zftdQzC0nbFt6BAJM52tiRsM0y5pcEfTl7y2bKwjFBSBwj3ik1P1yPTz6mP2h1xHEWoeJxPHdvujlZXJv8ObZO0PbHSPMk6xtnEmEqPAfPLzxjOzu63P3K_0eFdpgR48fUbcQwZt7yZkGzOPqYuUDAE7CBmvgvwRfwymkEzTD8ESt0vYvZdmoYjV7sbScmhoxYbWmjMatFvOzha6D1YA="),
    ("Q05", "gAAAAABqE-m-KRbrY2MpEseeszU46iQWHzbzwOO5-t10vHJrdQOKeaVwPxyp9kiBDCS1Fa5MJyQoTOp2pdEtw9LtUbCEJ_56caOBjtBgngLz4kvcodhVECBLBuD6vsCaQlopu0SardsvA3slA379M8nrcyuuea3dJ97FPlOdQs2b70BRPyOkyNH0nKGqBwQzBlAW7B-ucZwf9dDPPAw-xUTfR3ekIqXReQ=="),
    ("Q06", "gAAAAABqE-m-EYfgWBpxkb_5hGOvvBsAdBu5367Nd5d4uT_6EEAaTeCidG99u5XJ5vcZatZpoj5RjmfrY5O1XNObuApuq_ZFah_StEcLHB31Ow6WRrZpikDGUFJkC-ZfY0TggJzDFvdtwQsIttqNW5js0LMS-74V-AUx0UCi4bABm1vOMGBKP2qGyGTfyh2wfETTw4nNhbac"),
    ("Q07", "gAAAAABqE-m-cZLyG6To-HyWWdEYu42VgbV9c_SCWXt4qJE02YrOFvfMntuBTf-CVXt3MhJWFzrukGMR0-Brla1QMVbefRelzpJqkY2TsIQ3Tcc5MZ0BH6ornHjZAnOd9Iozf1f755EC8hBase1XtbhThrKgYJRKWPxaxKd-nkLK3XuabtmEF8r0bZtTyKVjYNBUWPT--lKJb-pXvw3p3zJ0z6utBLWicmBhgdJvGMoOQCsCLrxi6jrtHZzka7Me7Vm6UUhwSkdz"),
    ("Q08", "gAAAAABqE-m-sxXijCcjguEWTh7qgKt7BX4cbUfFdUwAz6VqSoU4fTnYXUhf-dVQdCKa1lhgc7ZZatU5Pu9iuQHG-ApZCOw2yR-PkZnuY9L7uR02CCJoWYhFQelqYEWYA5uONridoCzD8kh2yqwUSVInEFfBuB2cYgyPobRnP_yRvtaFtLakrMy0fsCZH_zfyrOMVkdF5GoHdPu67XzoEj806x4aS8DJ4ysYFuwNb9zkhhceq_CsU08="),
    ("Q09", "gAAAAABqE-m-nDGYgCF3fSWs2tM39pdnsBua61Ht1ruTZ_NOUmju6AxbGU6WB8HzLEHKQkkCnxc4ka2DohiUSLwVDrWG2ZnGggyt7OnI6D43ovjDBsMhW2jQPaz9zaHua25abfEqF4V1ZioQrdL7lz3D0qzDsjXl4Kw5RY2g3kaDakb62Cb6Dt8badoS-t4Bd_fEAp49t09FH_qwLp_ZTotiFsKFy6QADA=="),
    ("Q10", "gAAAAABqE-m-PwoVsLjWO4nbO8W_65P-UNNF7SjdNZL4sRN-G72eHygPuGyggXwVG8G7HJ2ZmrtCYuNg-rtWH_iuyexPQLVG0EqKr0ZQswJox4iauvFf014qlqr5vC_TtdwHGcMiZsyWZpJauDTffKDm_QJHrGElPUUunCFgX8356s1yMocleGXUBfcZ8B73A5LIALAXRIBpKyt707qYlLhwOG1vhsdR74q21NS0-n0skLZIy7z0pLM="),
    ("Q11", "gAAAAABqE-m-1BAGkhsZEDnkbSwAAwusmnMKdn2gvIM5tltaZ1W-eoKtvbPNu8rkAlOOiOW-9_NobJqDFKDO3J7zCPwWuEdGxwgYpX5sxh2Rg4ngR5R5WDnQsQTPIRHXJkkaN1ufNhvbQ-XOn2Z1QPci8118ByVpkAR5kZTUXOFIZ1IgHP2hbvO4E81GB9CTs9HiZvHAsAnS"),
    ("Q12", "gAAAAABqE-m-NrwI-KspXny9JlQqBEW_eB9jE6bGmnin6IX6SdcB9ol1gR7CmzczDKE6A7XHDOJW20tVHAlGFw-q-J6cWrTajK_mJTv00aHllSozrKiThojuxxnSjhgOhgtNKU5mh7zoz2d2uLo7p-Kl32m4IU6PRsm0kZceID-ZH5ZRw7w4h1qSZOufZO2HvKkR9LtfCQXk"),
    ("Q13", "gAAAAABqE-m-Xr56G8qaFfk3BIVQeDzP5mpahd7wZQ5vGR11AN_sxU1ZzjoPfbSdLmrrhFHEI8S8KhXfjOWZQoMJToWSsnhjZQdrRj0wujH38p2VOZLqqZYSmOflVEQm29z9pAXx_iltLWZLNGf8QsMtZWuo-3SsWt6R2mGvOMBTDj5hCzaq842_r1eupRQJJ1dnTSmNPskW"),
    ("Q14", "gAAAAABqE-m--oxJAL26EQ6bMS5vmgI0pWMWjgbG49qNZu8K_pIiDrp3ro1YFlVvBXOOJ6bSpI7lxz-OXmNrVFkSfJlVf4PchVKfWdddKVT85AMxUHo3PYD15IGV476RznHCiD59twp7x_E6HOF7AFUGiWcsO9Ph63Tfcvh3aJzF7Hk_NPEHcIaaEU9ki2eccYXehJJ3tkmr"),
    ("Q15", "gAAAAABqE-m-3JNAfb2dmCF-2XlNe-F1AaeXybgSJ4DwHtn9o52TEryPYgu-6m70Ivn7izeLy4h44AVbHL_3cv-MWfAwFYp7ct3lvF7dL1QbmhntyeY4c7l0CVPsc-mv8WuY04tpB2XPtHE_0ytl9tQlqAGonC2esnpMbSzgvZPdSw9eHnm5k2Jkh0FbgjLKNWxjdX3Uv2aYDiqOeLMQKZsMMteZzJcwHQ=="),
]

# Load fresh RAG answers from answers_preview.json
preview_path = Path(__file__).parent / "answers_preview.json"
rag_answers = {item["question_id"]: item["answer"] for item in json.loads(preview_path.read_text())}

questions = {qid: fernet.decrypt(enc.encode()).decode() for qid, enc in _Q}
out_dir = Path(__file__).parent

# Save as answers_v10.json
answers_v10 = [{"question_id": qid, "question": questions[qid], "answer": rag_answers[qid]} for qid, _ in _Q]
(out_dir / "answers_v10.json").write_text(json.dumps(answers_v10, indent=2, ensure_ascii=False))
print("answers_v10.json saved")

# Generate submission.csv
csv_path = out_dir / "submission.csv"
rows = []
for qid, enc in _Q:
    rows.append({
        "question_id": qid,
        "question_enc": fernet.encrypt(questions[qid].encode()).decode(),
        "answer_enc": fernet.encrypt(rag_answers[qid].encode()).decode(),
        "streamlit_link": STREAMLIT_URL,
        "langsmith_link": LANGSMITH_URL,
    })

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["question_id","question_enc","answer_enc","streamlit_link","langsmith_link"])
    writer.writeheader()
    writer.writerows(rows)

print(f"submission.csv generated — {len(rows)} rows")
for r in rows:
    print(f"  {r['question_id']}: {rag_answers[r['question_id']][:80].replace(chr(10),' | ')}...")
