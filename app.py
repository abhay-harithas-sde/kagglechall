"""
Zyro Dynamics HR Help Desk - Streamlit Chatbot App
RAG-powered HR assistant using FAISS + Groq + LangChain
"""

import os
import streamlit as st
from pathlib import Path

# ── LangChain / FAISS / Groq imports ────────────────────────────────────────
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain.schema import Document

# ── Streamlit page config ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Zyro Dynamics HR Help Desk",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d6a9f 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .main-header h1 { margin: 0; font-size: 1.8rem; }
    .main-header p  { margin: 0.3rem 0 0; opacity: 0.85; font-size: 0.95rem; }

    .source-card {
        background: #f0f7ff;
        border-left: 4px solid #2d6a9f;
        border-radius: 6px;
        padding: 0.6rem 1rem;
        margin: 0.4rem 0;
        font-size: 0.82rem;
        color: #333;
    }
    .out-of-scope {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        border-radius: 6px;
        padding: 0.6rem 1rem;
        margin: 0.4rem 0;
    }
    .chat-stats {
        font-size: 0.78rem;
        color: #888;
        text-align: right;
        margin-top: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Constants ────────────────────────────────────────────────────────────────
PDF_DIR = Path("/kaggle/input/niat-masterclass-rag-challenge")   # Kaggle dataset path
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
TOP_K = 5
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Out-of-scope topic keywords (fast pre-check before LLM)
OUT_OF_SCOPE_KEYWORDS = [
    "stock price", "share price", "revenue", "profit", "quarterly", "fiscal",
    "weather", "cricket", "sports", "movie", "recipe", "cook",
    "competitor", "market cap", "investment", "trading",
    "covid", "pandemic", "election", "politics", "religion",
    "personal loan", "bank account", "credit card",
]

# ── Helper: load & build RAG pipeline (cached) ──────────────────────────────
@st.cache_resource(show_spinner="Building HR knowledge base … this may take a minute ⏳")
def build_rag_pipeline():
    """Load PDFs → chunk → embed → FAISS → RAG chain."""
    groq_api_key = os.environ.get("GROQ_API_KEY", st.secrets.get("GROQ_API_KEY", ""))
    if not groq_api_key:
        st.error("⚠️  GROQ_API_KEY not found. Add it in Streamlit secrets or environment variables.")
        st.stop()

    # ── 1. Load PDFs ──────────────────────────────────────────────────────────
    pdf_files = list(PDF_DIR.glob("*.pdf"))
    if not pdf_files:
        # Fallback: look in the same directory as app.py
        pdf_files = list(Path(__file__).parent.glob("*.pdf"))

    if not pdf_files:
        st.error(f"No PDF files found in {PDF_DIR}. Please make sure the dataset is attached.")
        st.stop()

    docs: list[Document] = []
    for pdf in pdf_files:
        try:
            loader = PyPDFLoader(str(pdf))
            pages = loader.load()
            # tag each page with its source filename
            for page in pages:
                page.metadata["source_file"] = pdf.name
            docs.extend(pages)
        except Exception as e:
            st.warning(f"Could not load {pdf.name}: {e}")

    # ── 2. Chunk documents ────────────────────────────────────────────────────
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    chunks = splitter.split_documents(docs)

    # ── 3. Embed & build FAISS vector store ───────────────────────────────────
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    vectorstore = FAISS.from_documents(chunks, embeddings)

    # MMR retriever for diverse, relevant chunks
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": TOP_K, "fetch_k": 20, "lambda_mult": 0.6},
    )

    # ── 4. LLM ───────────────────────────────────────────────────────────────
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=groq_api_key,
        temperature=0.1,
        max_tokens=1024,
    )

    # ── 5. Prompt ─────────────────────────────────────────────────────────────
    system_prompt = """You are an expert HR Help Desk assistant for Zyro Dynamics Pvt. Ltd.
Your job is to answer employee questions ONLY based on the provided HR policy documents.

Guidelines:
- Answer clearly and accurately using ONLY the retrieved context below.
- If the context does not contain enough information, say so honestly.
- Do NOT fabricate information or use outside knowledge.
- Format lists and steps clearly when appropriate.
- Keep answers concise but complete.

Retrieved Context:
{context}
"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}"),
    ])

    # ── 6. LCEL RAG chain ─────────────────────────────────────────────────────
    def format_docs(docs):
        return "\n\n---\n\n".join(
            f"[Source: {d.metadata.get('source_file','unknown')} | Page {d.metadata.get('page','')+1}]\n{d.page_content}"
            for d in docs
        )

    rag_chain = (
        RunnablePassthrough.assign(
            context=lambda x: format_docs(retriever.invoke(x["question"]))
        )
        | prompt
        | llm
        | StrOutputParser()
    )

    return retriever, rag_chain, len(pdf_files), len(chunks)


def is_out_of_scope(question: str) -> bool:
    """Quick keyword-based out-of-scope pre-check."""
    q_lower = question.lower()
    return any(kw in q_lower for kw in OUT_OF_SCOPE_KEYWORDS)


def get_answer(question: str, retriever, rag_chain) -> dict:
    """
    Returns dict with keys: answer, sources, out_of_scope
    """
    # Fast pre-check
    if is_out_of_scope(question):
        return {
            "answer": (
                "I'm sorry, but I can only answer HR-related questions based on "
                "Zyro Dynamics' internal policy documents. Your question appears to be "
                "outside the scope of our HR knowledge base. Please reach out to the "
                "appropriate department for assistance."
            ),
            "sources": [],
            "out_of_scope": True,
        }

    # Retrieve relevant chunks
    source_docs = retriever.invoke(question)

    # If no meaningful context found, treat as out-of-scope
    if not source_docs:
        return {
            "answer": (
                "I couldn't find relevant information in the HR policy documents "
                "to answer your question. This may be outside the scope of our HR "
                "knowledge base."
            ),
            "sources": [],
            "out_of_scope": True,
        }

    # Generate answer
    answer = rag_chain.invoke({"question": question})

    # LLM-level out-of-scope detection (if LLM says it can't answer)
    refusal_phrases = [
        "i cannot answer", "outside my scope", "not covered", "cannot find",
        "no information", "not available in the provided", "unable to find",
    ]
    if any(phrase in answer.lower() for phrase in refusal_phrases):
        return {
            "answer": answer,
            "sources": [],
            "out_of_scope": True,
        }

    # Build unique source list
    seen = set()
    sources = []
    for doc in source_docs:
        key = (doc.metadata.get("source_file", ""), doc.metadata.get("page", ""))
        if key not in seen:
            seen.add(key)
            sources.append({
                "file": doc.metadata.get("source_file", "Unknown"),
                "page": doc.metadata.get("page", 0) + 1,
                "snippet": doc.page_content[:200].replace("\n", " ") + "…",
            })

    return {"answer": answer, "sources": sources, "out_of_scope": False}


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏢 Zyro Dynamics")
    st.markdown("**HR Help Desk Assistant**")
    st.divider()

    # Build pipeline
    retriever, rag_chain, n_pdfs, n_chunks = build_rag_pipeline()

    st.success(f"✅ Knowledge base ready")
    st.markdown(f"- 📄 **{n_pdfs}** policy documents loaded")
    st.markdown(f"- 🔢 **{n_chunks:,}** text chunks indexed")
    st.divider()

    st.markdown("### 📚 Available Policies")
    policies = [
        "Company Profile", "Employee Handbook", "Leave Policy",
        "Work From Home Policy", "Code of Conduct", "Performance Review Policy",
        "Compensation & Benefits Policy", "IT & Data Security Policy",
        "POSH Policy", "Onboarding & Separation Policy", "Travel & Expense Policy",
    ]
    for p in policies:
        st.markdown(f"• {p}")

    st.divider()
    st.markdown("### 💡 Sample Questions")
    sample_qs = [
        "How many casual leaves do I get per year?",
        "What is the work from home policy?",
        "How is the annual performance review conducted?",
    ]
    for q in sample_qs:
        if st.button(q, key=f"sample_{q[:20]}", use_container_width=True):
            st.session_state["prefill"] = q

    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()

# ── Main area ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🏢 Zyro Dynamics HR Help Desk</h1>
    <p>Ask me anything about company HR policies — Leave, WFH, Performance, Benefits & more</p>
</div>
""", unsafe_allow_html=True)

# Init chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("sources"):
            with st.expander(f"📎 Sources ({len(msg['sources'])} chunks)", expanded=False):
                for src in msg["sources"]:
                    st.markdown(
                        f'<div class="source-card">📄 <b>{src["file"]}</b> — Page {src["page"]}<br>'
                        f'<i>{src["snippet"]}</i></div>',
                        unsafe_allow_html=True,
                    )

# Chat input (with optional prefill from sidebar sample button)
prefill = st.session_state.pop("prefill", "")
user_input = st.chat_input("Ask an HR question…", key="chat_input") or prefill

if user_input:
    # Show user message
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate answer
    with st.chat_message("assistant"):
        with st.spinner("Searching HR policies…"):
            result = get_answer(user_input, retriever, rag_chain)

        if result["out_of_scope"]:
            st.markdown(
                f'<div class="out-of-scope">⚠️ {result["answer"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(result["answer"])
            if result["sources"]:
                with st.expander(f"📎 Sources ({len(result['sources'])} chunks)", expanded=False):
                    for src in result["sources"]:
                        st.markdown(
                            f'<div class="source-card">📄 <b>{src["file"]}</b> — Page {src["page"]}<br>'
                            f'<i>{src["snippet"]}</i></div>',
                            unsafe_allow_html=True,
                        )

    # Save to history
    st.session_state["messages"].append({
        "role": "assistant",
        "content": result["answer"],
        "sources": result.get("sources", []),
    })

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#888; font-size:0.8rem;'>"
    "Zyro Dynamics HR Help Desk · Powered by RAG + Groq · Built with ❤️ using LangChain & Streamlit"
    "</div>",
    unsafe_allow_html=True,
)
