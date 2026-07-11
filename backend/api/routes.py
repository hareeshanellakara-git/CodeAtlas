

from fastapi import APIRouter, HTTPException
from backend.config import Settings
from backend.api.schemas import (
    ChatRequest,
    ChatResponse,
    IngestRequest,
    IngestResponse,
)
from backend.services.chat_service import ChatService
from backend.services.github_service import GitHubService

router = APIRouter()


@router.post(
    "/ingest",
    response_model=IngestResponse,
)
def ingest_repository(request: IngestRequest):

    try:

        github_service = GitHubService()

        result = github_service.ingest_repository(
            str(request.repository_url)
        )

        return IngestResponse(
            message=(
                f"Repository '{result['repository']}' "
                "indexed successfully."
            ),
            repository=result["repository"],

            documents_processed=result["documents_processed"],

            chunks_created=result["chunks_created"],

            embedding_model=Settings.EMBEDDING_MODEL,

            vector_database="FAISS",

            llm=Settings.LLM_MODEL,
        )

    except Exception as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )


@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):

    try:

        chat_service = ChatService()

        result = chat_service.ask(
            request.question
        )

        sources = []

        if "context" in result:

            sources = list(
                {
                    document.metadata.get(
                        "source",
                        "Unknown",
                    )
                    for document in result["context"]
                }
            )

        return ChatResponse(
            answer=result["answer"],
            sources=sources,
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )