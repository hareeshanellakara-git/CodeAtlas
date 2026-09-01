from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import urlparse

import requests

from config import (
    INGEST_ENDPOINT,
    CHAT_ENDPOINT,
    IMPACT_ENDPOINT,
    REQUEST_TIMEOUT_INGEST,
    REQUEST_TIMEOUT_CHAT,
    REQUEST_TIMEOUT_IMPACT,
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
        """True when the backend returns document and chunk counts."""

        return (
            self.documents_processed is not None
            and self.chunks_created is not None
        )


@dataclass
class ChatResult:

    answer: str

    sources: list = field(
        default_factory=list
    )


@dataclass
class ImpactResult:

    repository: str

    changed_file: str

    direct_dependents: list = field(
        default_factory=list
    )

    indirect_dependents: list = field(
        default_factory=list
    )

    total_affected_files: int = 0

    all_affected_files: list = field(
        default_factory=list
    )


def _repo_name_from_url(
    repo_url: str,
) -> str:
    """
    Convert:

        https://github.com/owner/repo

    into:

        owner/repo
    """

    path = urlparse(
        repo_url
    ).path.strip("/")

    return (
        path.removesuffix(".git")
        if path
        else repo_url
    )


def ingest_repository(
    repo_url: str,
) -> IngestResult:

    try:

        response = requests.post(
            INGEST_ENDPOINT,

            json={
                "repository_url": repo_url
            },

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

            raise APIError(
                detail
            )

    except APIError:

        raise

    except requests.exceptions.RequestException as exc:

        raise APIError(
            f"Could not reach the backend: {exc}"
        ) from exc

    data = response.json()

    return IngestResult(

        message=data.get(
            "message",
            "Repository indexed successfully.",
        ),

        repository=(
            data.get(
                "repository"
            )
            or _repo_name_from_url(
                repo_url
            )
        ),

        documents_processed=data.get(
            "documents_processed"
        ),

        chunks_created=data.get(
            "chunks_created"
        ),

        embedding_model=data.get(
            "embedding_model",
            "",
        ),

        vector_database=data.get(
            "vector_database",
            "",
        ),

        llm=data.get(
            "llm",
            "",
        ),

        repository_intelligence=data.get(
            "repository_intelligence",
            {},
        ),
    )


def ask_question(
    question: str,
) -> ChatResult:

    try:

        response = requests.post(
            CHAT_ENDPOINT,

            json={
                "question": question
            },

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

            raise APIError(
                detail
            )

    except APIError:

        raise

    except requests.exceptions.RequestException as exc:

        raise APIError(
            "Unable to connect to the backend server: "
            f"{exc}"
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


def analyze_impact(
    repository: str,
    changed_file: str,
) -> ImpactResult:

    try:

        response = requests.post(
            IMPACT_ENDPOINT,

            json={
                "repository": repository,
                "changed_file": changed_file,
            },

            timeout=REQUEST_TIMEOUT_IMPACT,
        )

        if not response.ok:

            try:

                detail = response.json().get(
                    "detail",
                    "Impact analysis failed.",
                )

            except Exception:

                detail = response.text

            raise APIError(
                detail
            )

    except APIError:

        raise

    except requests.exceptions.RequestException as exc:

        raise APIError(
            "Unable to connect to the backend server: "
            f"{exc}"
        ) from exc

    data = response.json()

    return ImpactResult(

        repository=data.get(
            "repository",
            repository,
        ),

        changed_file=data.get(
            "changed_file",
            changed_file,
        ),

        direct_dependents=data.get(
            "direct_dependents",
            [],
        ),

        indirect_dependents=data.get(
            "indirect_dependents",
            [],
        ),

        total_affected_files=data.get(
            "total_affected_files",
            0,
        ),

        all_affected_files=data.get(
            "all_affected_files",
            [],
        ),
    )