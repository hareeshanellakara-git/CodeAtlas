from typing import Any

from pydantic import BaseModel, HttpUrl


class IngestRequest(BaseModel):

    repository_url: HttpUrl


class IngestResponse(BaseModel):

    message: str

    repository: str

    documents_processed: int

    chunks_created: int

    embedding_model: str

    vector_database: str

    llm: str

    repository_intelligence: dict[str, Any]


class ChatRequest(BaseModel):

    question: str






class ImpactRequest(BaseModel):

    repository: str

    changed_file: str


class ImpactResponse(BaseModel):

    repository: str

    changed_file: str

    direct_dependents: list[str]

    indirect_dependents: list[str]

    total_affected_files: int

    all_affected_files: list[str]


class EvidenceItem(BaseModel):
    rank: int
    source: str
    score: float
    preview: str

class ChatResponse(BaseModel):

    answer: str

    sources: list[str]

    evidence: list[EvidenceItem]