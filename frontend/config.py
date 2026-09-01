
import os


API_BASE_URL = os.getenv("CODEATLAS_API_URL", "http://localhost:8000")
INGEST_ENDPOINT = f"{API_BASE_URL}/ingest"
CHAT_ENDPOINT = f"{API_BASE_URL}/chat"

REQUEST_TIMEOUT_INGEST = 180  # cloning + embedding can take a while
REQUEST_TIMEOUT_CHAT = 60


APP_NAME = "CodeAtlas"
APP_TAGLINE = "AI-powered GitHub Repository Assistant"
APP_DESCRIPTION = (
    "Understand any GitHub repository in seconds using Retrieval-Augmented Generation."
)
LOGO_PATH = "frontend/assets/logo.png"
LOGO_PATH2 = "frontend/assets/logo2.png"
CSS_PATH = "frontend/styles/style.css"


DEFAULT_EMBEDDING_MODEL = "FastEmbed (BAAI/bge-small-en-v1.5)"
DEFAULT_LLM = "GPT-OSS 120B (Groq)"
DEFAULT_VECTOR_DB = "FAISS"

POWERED_BY = ["LangChain", "Groq", "FAISS", "FastEmbed", "FastAPI", "Streamlit"]



IMPACT_ENDPOINT = f"{API_BASE_URL}/impact"

REQUEST_TIMEOUT_IMPACT = 30