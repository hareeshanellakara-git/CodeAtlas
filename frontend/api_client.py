
from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import urlparse

import requests

from config import (
    INGEST_ENDPOINT,
    CHAT_ENDPOINT,
    REQUEST_TIMEOUT_INGEST,
    REQUEST_TIMEOUT_CHAT,
)


class APIError(Exception):
    """Raised whenever the backend can't be reached or returns an error."""


@dataclass
class IngestResult:
    message: str
    repository: str = ""
    documents_processed: Optional[int] = None
    chunks_created: Optional[int] = None
    embedding_model: str = ""
    vector_database: str = ""
    llm: str = ""
    repository_intelligence: dict = field(
        default_factory=dict
    )

    @property
    def has_detailed_stats(self) -> bool:
        """True once the backend starts returning real chunk/doc counts."""
        return self.documents_processed is not None and self.chunks_created is not None


@dataclass
class ChatResult:
    answer: str
    sources: list = field(default_factory=list)


def _repo_name_from_url(repo_url: str) -> str:
    """'https://github.com/owner/repo' -> 'owner/repo'."""
    path = urlparse(repo_url).path.strip("/")
    return path.removesuffix(".git") if path else repo_url


def ingest_repository(repo_url: str) -> IngestResult:
    
    try:
        response = requests.post(
            INGEST_ENDPOINT,
            json={"repository_url": repo_url},
            timeout=REQUEST_TIMEOUT_INGEST,
        )
        if not response.ok:
            try:
                detail = response.json().get(
                    "detail",
                    "Something went wrong.",
                )
            except Exception:
                detail = response.text

            raise APIError(detail)

    except APIError:
        raise
    except requests.exceptions.RequestException as exc:
        raise APIError(f"Could not reach the backend: {exc}") from exc

    data = response.json()
    return IngestResult(
        message=data.get("message", "Repository indexed successfully."),
        repository=data.get("repository") or _repo_name_from_url(repo_url),
        documents_processed=data.get("documents_processed"),
        chunks_created=data.get("chunks_created"),
        embedding_model=data.get("embedding_model", ""),
        vector_database=data.get("vector_database", ""),
        llm=data.get("llm", ""),
        repository_intelligence=data.get(
            "repository_intelligence",
            {},
        ),
    )


def ask_question(question: str) -> ChatResult:

    try:
        response = requests.post(
            CHAT_ENDPOINT,
            json={"question": question},
            timeout=REQUEST_TIMEOUT_CHAT,
        )

        if not response.ok:
            try:
                detail = response.json().get(
                    "detail",
                    "Something went wrong.",
                )
            except Exception:
                detail = response.text

            raise APIError(detail)

    except APIError:
        raise

    except requests.exceptions.RequestException as exc:
        raise APIError(
            f"Unable to connect to the backend server: {exc}"
        ) from exc

    data = response.json()

    return ChatResult(
        answer=data.get(
            "answer",
            "I couldn't generate an answer.",
        ),
        sources=data.get(
            "sources",
            [],
        ),
    )