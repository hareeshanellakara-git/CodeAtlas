from backend.loaders.github_loader import GitHubLoader
from backend.loaders.document_loader import DocumentLoader

from backend.services.chunking_service import ChunkingService
from backend.services.vectorstore_service import VectorStoreService

from backend.repository_intelligence.repository_analyzer import (
    RepositoryAnalyzer,
)
from backend.repository_intelligence.analysis_store import (
    AnalysisStore,
)


class GitHubService:

    def __init__(self):

        self.github_loader = GitHubLoader()

        self.document_loader = DocumentLoader()

        self.chunking_service = ChunkingService()

        self.vectorstore_service = (
            VectorStoreService()
        )

        self.repository_analyzer = (
            RepositoryAnalyzer()
        )
        self.analysis_store = AnalysisStore()

    def ingest_repository(
        self,
        repo_url: str,
    ):

        repo_path = (
            self.github_loader.clone_repo(
                repo_url
            )
        )

        repository_intelligence = (
            self.repository_analyzer
            .analyze_repository(
                repo_path
            )
        )


        repository_name = (
            repo_url.rstrip("/")
            .split("/")[-1]
        )

        if repository_name.endswith(".git"):
            repository_name = repository_name[:-4]

        repository_intelligence[
            "repository_name"
        ] = repository_name

        self.analysis_store.save(
            repository_name,
            repository_intelligence,
        )


        documents = (
            self.document_loader.load_repository(
                repo_path
            )
        )

        chunks = (
            self.chunking_service.split_documents(
                documents
            )
        )

        self.vectorstore_service.create_vectorstore(
            chunks
        )

        

        return {
            "status": "success",

            "repository": repository_name,

            "documents_processed": len(
                documents
            ),

            "chunks_created": len(
                chunks
            ),

            "repository_intelligence": (
                repository_intelligence
            ),
        }