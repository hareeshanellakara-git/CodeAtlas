from fastapi import APIRouter, HTTPException

from backend.config import Settings

from backend.api.schemas import (
    ChatRequest,
    ChatResponse,
    IngestRequest,
    IngestResponse,
    ImpactRequest,
    ImpactResponse,
    SRSRequest,
    SRSResponse,
)

from backend.services.chat_service import ChatService
from backend.services.github_service import GitHubService

from backend.repository_intelligence.analysis_store import (
    AnalysisStore,
)

from backend.repository_intelligence.impact_analyzer import (
    ImpactAnalyzer,
)
from backend.repository_intelligence.srs.srs_generator import (
    SRSGenerator,
)

router = APIRouter()


@router.post(
    "/ingest",
    response_model=IngestResponse,
)
def ingest_repository(
    request: IngestRequest,
):

    try:

        github_service = GitHubService()

        result = (
            github_service.ingest_repository(
                str(request.repository_url)
            )
        )

        return IngestResponse(
            message=(
                f"Repository '{result['repository']}' "
                "indexed successfully."
            ),

            repository=result["repository"],

            documents_processed=(
                result["documents_processed"]
            ),

            chunks_created=(
                result["chunks_created"]
            ),

            embedding_model=(
                Settings.EMBEDDING_MODEL
            ),

            vector_database="FAISS",

            llm=Settings.LLM_MODEL,

            repository_intelligence=(
                result[
                    "repository_intelligence"
                ]
            ),
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
def chat(
    request: ChatRequest,
):

    try:

        chat_service = ChatService()

        result = chat_service.ask(
            request.question
        )

        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
            evidence=result["evidence"],
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )

@router.post(
    "/impact",
    response_model=ImpactResponse,
)
def analyze_impact(
    request: ImpactRequest,
):

    try:

        analysis_store = AnalysisStore()

        analysis = analysis_store.load(
            request.repository
        )

        dependency_edges = analysis.get(
            "dependency_edges",
            [],
        )

        analyzer = ImpactAnalyzer()

        result = analyzer.analyze(
            dependency_edges,
            request.changed_file,
        )

        return ImpactResponse(
            repository=request.repository,

            changed_file=result[
                "changed_file"
            ],

            direct_dependents=result[
                "direct_dependents"
            ],

            indirect_dependents=result[
                "indirect_dependents"
            ],

            total_affected_files=result[
                "total_affected_files"
            ],

            all_affected_files=result[
                "all_affected_files"
            ],
        )

    except FileNotFoundError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


@router.post(
    "/srs",
    response_model=SRSResponse,
)
def generate_srs(
    request: SRSRequest,
):

    try:

        analysis_store = AnalysisStore()

        analysis = analysis_store.load(
            request.repository
        )

        generator = SRSGenerator()

        document = generator.generate(
            analysis
        )

        return SRSResponse(
            repository=request.repository,
            document=document,
        )

    except FileNotFoundError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )