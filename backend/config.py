import os

from dotenv import load_dotenv

load_dotenv()


class Settings:

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    LLM_MODEL = "llama-3.3-70b-versatile"

    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

    REPO_STORAGE_PATH = "data/repos"

    VECTORSTORE_PATH = "data/vectorstore"

    ALLOWED_EXTENSIONS = {
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".java",
        ".cpp",
        ".c",
        ".cs",
        ".go",
        ".rs",
        ".php",
        ".html",
        ".css",
        ".md",
        ".json",
        ".yaml",
        ".yml",
        ".txt",
    }

    EXCLUDED_DIRECTORIES = {
        ".git",
        "__pycache__",
        "node_modules",
        "dist",
        "build",
        ".venv",
        "venv",
        ".idea",
        ".vscode",
    }

settings = Settings()