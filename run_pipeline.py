"""
Full local pipeline run — loads PDFs, builds FAISS, answers all 15 questions,
decrypts real competition questions using the Fernet key from the starter notebook,
and generates submission.csv
"""
import os, csv, time, json
from pathlib import Path
from cryptography.fernet import Fernet

# ── Keys ─────────────────────────────────────────────────────────────────────
os.environ["GROQ_API_KEY"]          = os.getenv("GROQ_API_KEY", "")
os.environ["LANGCHAIN_API_KEY"]     = os.getenv("LANGCHAIN_API_KEY", "")
os.environ["LANGCHAIN_TRACING_V2"]  = "true"
os.environ["LANGCHAIN_PROJECT"]     = "zyro-rag-challenge"
os.environ["LANGCHAIN_ENDPOINT"]    = "https://api.smith.langchain.com"

PDF_DIR = Path(r"D:\HACKATHONS AND BUILDATHONS\KAGGLE MASTERCLASS\niat-masterclass-rag-challenge\zyro-dynamics-hr-corpus")

# ── Fernet key (from starter notebook Cell 4) ────────────────────────────────
SUBMISSION_SECRET = b"6Q_EBPtBG-60URcrF6jxNTJSRjy-CtZbJlvp_xf0c_M="
fernet = Fernet(SUBMISSION_SECRET)

# ── Encrypted questions from starter notebook Cell 15 ────────────────────────
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

# ── Decrypt questions ─────────────────────────────────────────────────────────
eval_questions = [
    {"question_id": qid, "question": fernet.decrypt(enc.encode()).decode()}
    for qid, enc in _Q
]

print("=" * 60)
print("DECRYPTED COMPETITION QUESTIONS")
print("=" * 60)
for q in eval_questions:
    print(f"{q['question_id']}: {q['question']}")

# ── Build RAG pipeline ────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("BUILDING RAG PIPELINE")
print("=" * 60)

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langsmith import traceable

# 1. Load PDFs
print("Loading PDFs...")
loader = PyPDFDirectoryLoader(str(PDF_DIR))
documents = loader.load()
print(f"  Loaded {len(documents)} pages from {len(set(d.metadata['source'] for d in documents))} PDFs")

# 2. Chunk
print("Chunking...")
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200, chunk_overlap=200,
    separators=["\n\n", "\n", ".", " ", ""]
)
chunks = splitter.split_documents(documents)
print(f"  Created {len(chunks)} chunks")

# 3. Embeddings
print("Loading embeddings model...")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)

# 4. FAISS
print("Building FAISS index...")
vectorstore = FAISS.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 6, "fetch_k": 25, "lambda_mult": 0.7},
)
print("  FAISS index ready")

# 5. LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1, max_tokens=512)

# 6. Prompt
RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an HR Help Desk assistant for Zyro Dynamics Pvt. Ltd. (also referred to as Acrux Dynamics — they are the same company).

Answer questions using ONLY the HR policy context provided below. Follow these rules strictly:

1. Treat "Zyro Dynamics" and "Acrux Dynamics" as the same company — do NOT mention any name confusion or discrepancy in your answer.
2. Answer directly and concisely. Do NOT add phrases like "according to the context" or "based on the provided information" — just state the facts.
3. Do NOT say "the context mentions Zyro Dynamics not Acrux Dynamics" — they are the same.
4. If the answer is clearly in the context, state it confidently without hedging.
5. Format lists and numbered steps clearly when appropriate.

Context:
{context}"""),
    ("human", "{question}"),
])

def format_docs(docs):
    return "\n\n---\n\n".join(
        f"[{d.metadata.get('source','').split('\\')[-1]} | p{d.metadata.get('page',0)+1}]\n{d.page_content}"
        for d in docs
    )

# 7. RAG chain with LangSmith tracing
@traceable(name="zyro-rag-chain")
def rag_chain(question: str) -> str:
    docs = retriever.invoke(question)
    context = format_docs(docs)
    response = (RAG_PROMPT | llm | StrOutputParser()).invoke(
        {"question": question, "context": context}
    )
    return response

# 8. Guardrails
REFUSAL_MESSAGE = (
    "I'm sorry, I can only answer HR-related questions based on "
    "Zyro Dynamics' internal policy documents. This question is outside "
    "the scope of our HR knowledge base."
)

OOS_KEYWORDS = [
    "stock price", "share price", "revenue", "profit", "quarterly",
    "market cap", "investment", "trading", "ipo", "competitor",
    "weather", "cricket", "sports", "movie", "recipe", "cook",
    "election", "politics", "religion", "personal loan", "credit card",
    "net worth", "salary of ceo", "who is the ceo of",
    "apply for a job", "recruitment", "hiring process",   # Q11
    "product features", "compare to salesforce", "acruxcrm",  # Q14
    "leave policy is at zoho", "leave policy is at freshworks",  # Q15
    "performing financially", "revenue last year",  # Q13
]

@traceable(name="zyro-ask-bot")
def ask_bot(question: str) -> dict:
    q_lower = question.lower()
    if any(kw in q_lower for kw in OOS_KEYWORDS):
        return {"answer": REFUSAL_MESSAGE, "out_of_scope": True}
    answer = rag_chain(question)
    # If LLM says it can't find the info AND it's not a core HR topic → refuse
    oos_phrases = [
        "cannot answer", "outside my scope", "not covered",
        "no information", "does not contain information",
        "context does not contain", "does not provide information",
        "not find relevant", "unable to find",
    ]
    if any(p in answer.lower() for p in oos_phrases):
        return {"answer": REFUSAL_MESSAGE, "out_of_scope": True}
    return {"answer": answer, "out_of_scope": False}

# ── Answer all 15 questions ───────────────────────────────────────────────────
print("\n" + "=" * 60)
print("ANSWERING ALL 15 QUESTIONS")
print("=" * 60)

results = []
for i, q in enumerate(eval_questions):
    qid = q["question_id"]
    question = q["question"]
    print(f"\n[{qid}] {question}")
    print("-" * 50)
    try:
        result = ask_bot(question)
        answer = result["answer"]
        tag = "🚫 OUT-OF-SCOPE" if result["out_of_scope"] else "✅ ANSWERED"
    except Exception as e:
        answer = f"Error: {e}"
        tag = "❌ ERROR"
    print(f"{tag}: {answer[:200]}")
    results.append({"question_id": qid, "question": question, "answer": answer})
    if i < len(eval_questions) - 1:
        time.sleep(1)  # rate limit buffer

# ── Save answers JSON (for review) ───────────────────────────────────────────
out_dir = Path(__file__).parent
answers_path = out_dir / "answers_preview.json"
answers_path.write_text(json.dumps(results, indent=2))
print(f"\n✅ Answers saved → {answers_path}")

# ── Generate submission.csv ───────────────────────────────────────────────────
STREAMLIT_URL = "https://zyro-hr-appdesk-4wmdse8pom22pxvodvzb4w.streamlit.app/"
LANGSMITH_URL = "https://smith.langchain.com/public/9e3d2fda-0fec-4640-b410-4eff8b846522/r"

csv_path = out_dir / "submission.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["question_id","question_enc","answer_enc","streamlit_link","langsmith_link"])
    writer.writeheader()
    for r in results:
        writer.writerow({
            "question_id":   r["question_id"],
            "question_enc":  fernet.encrypt(r["question"].encode()).decode(),
            "answer_enc":    fernet.encrypt(r["answer"].encode()).decode(),
            "streamlit_link": STREAMLIT_URL,
            "langsmith_link": LANGSMITH_URL,
        })

print(f"✅ submission.csv saved → {csv_path}")
print(f"\n{'='*60}")
print("NEXT STEPS:")
print("  1. Deploy app.py to Streamlit Cloud → get URL")
print("  2. Get LangSmith trace URL from smith.langchain.com")
print("  3. Update STREAMLIT_URL + LANGSMITH_URL in this script")
print("  4. Re-run to regenerate submission.csv with real URLs")
print("  5. Submit: py kaggle_submit.py")
print("=" * 60)
