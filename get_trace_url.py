"""
Sends a traced RAG run to LangSmith and prints the shareable trace URL.
Run this AFTER the pipeline has run at least once.
"""
import os, time

os.environ["LANGCHAIN_API_KEY"]    = os.getenv("LANGCHAIN_API_KEY", "")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"]    = "zyro-rag-challenge"
os.environ["LANGCHAIN_ENDPOINT"]   = "https://api.smith.langchain.com"
os.environ["GROQ_API_KEY"]         = os.getenv("GROQ_API_KEY", "")

from pathlib import Path
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langsmith import Client, traceable

PDF_DIR = Path(r"D:\HACKATHONS AND BUILDATHONS\KAGGLE MASTERCLASS\niat-masterclass-rag-challenge\zyro-dynamics-hr-corpus")

print("Building pipeline...")
loader = PyPDFDirectoryLoader(str(PDF_DIR))
documents = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
chunks = splitter.split_documents(documents)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)
vectorstore = FAISS.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 5, "fetch_k": 20, "lambda_mult": 0.6})
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1, max_tokens=512)
prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer ONLY from the HR policy context below.\nContext: {context}"),
    ("human", "{question}"),
])

def fmt(docs):
    return "\n---\n".join(d.page_content for d in docs)

@traceable(name="zyro-hr-rag", project_name="zyro-rag-challenge")
def rag_chain(question: str) -> str:
    docs = retriever.invoke(question)
    return (prompt | llm | StrOutputParser()).invoke({"question": question, "context": fmt(docs)})

# Run 3 sample questions to generate traces
test_qs = [
    "At what rate does Earned Leave accrue per month and how many days per year?",
    "What is the maternity leave entitlement and eligibility requirement?",
    "What is the WFH policy and who is eligible?",
]

print("Sending traced runs to LangSmith...")
run_ids = []
for q in test_qs:
    print(f"  Q: {q[:60]}...")
    ans = rag_chain(q)
    print(f"  A: {ans[:80]}...")
    time.sleep(1)

# Wait for traces to propagate
print("\nWaiting for traces to sync...")
time.sleep(5)

# Fetch the latest run URL
client = Client()
runs = list(client.list_runs(project_name="zyro-rag-challenge", limit=5))
if runs:
    print(f"\nFound {len(runs)} traces in 'zyro-rag-challenge'")
    latest = runs[0]
    print(f"\nLatest run ID  : {latest.id}")
    print(f"Latest run name: {latest.name}")
    # Share the run (make it public)
    try:
        shared_url = client.share_run(latest.id)
        print(f"\n🔗 PUBLIC TRACE URL:\n   {shared_url}")
    except Exception as e:
        print(f"\nManual steps to get trace URL:")
        print(f"  1. Go to: https://smith.langchain.com")
        print(f"  2. Open project: zyro-rag-challenge")
        print(f"  3. Click any trace → Share → Enable Public Link → Copy URL")
else:
    print("No runs found yet — wait a moment and check smith.langchain.com manually")
