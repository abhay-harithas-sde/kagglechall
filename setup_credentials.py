"""
Run this script ONCE to set up Kaggle + Groq + LangSmith credentials.
Usage:  py setup_credentials.py
"""
import os
import json
import pathlib

print("=" * 55)
print("  Zyro Dynamics RAG Challenge — Credential Setup")
print("=" * 55)

# ── 1. Kaggle credentials ─────────────────────────────────────────────────────
print("\n📦 KAGGLE SETUP")
print("  Get your API key from: https://www.kaggle.com/settings → API → Create New Token")
kaggle_user = input("  Enter your Kaggle username: ").strip()
kaggle_key  = input("  Enter your Kaggle API key : ").strip()

kaggle_dir  = pathlib.Path.home() / ".kaggle"
kaggle_dir.mkdir(exist_ok=True)
kaggle_json = kaggle_dir / "kaggle.json"
kaggle_json.write_text(json.dumps({"username": kaggle_user, "key": kaggle_key}))
# Secure the file (important on Linux/Mac, harmless on Windows)
try:
    kaggle_json.chmod(0o600)
except Exception:
    pass
print(f"  ✅ Saved to {kaggle_json}")

# ── 2. Groq API key ───────────────────────────────────────────────────────────
print("\n🤖 GROQ SETUP")
print("  Get your free API key from: https://console.groq.com → API Keys")
groq_key = input("  Enter your Groq API key: ").strip()

# ── 3. LangSmith API key ──────────────────────────────────────────────────────
print("\n🔗 LANGSMITH SETUP")
print("  Get your free API key from: https://smith.langchain.com → Settings → API Keys")
langsmith_key = input("  Enter your LangSmith API key: ").strip()

# ── 4. Write a .env file for local use ───────────────────────────────────────
env_path = pathlib.Path(__file__).parent / ".env"
env_path.write_text(
    f"GROQ_API_KEY={groq_key}\n"
    f"LANGCHAIN_API_KEY={langsmith_key}\n"
    f"LANGCHAIN_TRACING_V2=true\n"
    f"LANGCHAIN_PROJECT=zyro-rag-challenge\n"
    f"LANGCHAIN_ENDPOINT=https://api.smith.langchain.com\n"
)
print(f"\n  ✅ Saved .env → {env_path}")

# ── 5. Verify Kaggle CLI ──────────────────────────────────────────────────────
print("\n🔍 Verifying Kaggle CLI...")
ret = os.system("py -m kaggle competitions list --csv 2>&1 | head -3")
if ret != 0:
    print("  ⚠️  Kaggle CLI test failed — check your username/key and try again")
else:
    print("  ✅ Kaggle CLI working!")

print("\n" + "=" * 55)
print("  All done! You can now run:")
print("  • py -m kaggle competitions list")
print("  • py -m streamlit run app.py")
print("=" * 55)
