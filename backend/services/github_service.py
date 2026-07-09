from backend.loaders.github_loader import GitHubLoader
from backend.loaders.document_loader import DocumentLoader

from backend.services.chunking_service import ChunkingService
from backend.services.vectorstore_service import VectorStoreService


class GitHubService:

    def __init__(self):

        self.github_loader = GitHubLoader()
        self.document_loader = DocumentLoader()
        self.chunking_service = ChunkingService()
        self.vectorstore_service = VectorStoreService()

    def ingest_repository(self, repo_url: str):

        repo_path = self.github_loader.clone_repo(repo_url)

        documents = self.document_loader.load_repository(
            repo_path
        )

        chunks = self.chunking_service.split_documents(
            documents
        )

        self.vectorstore_service.create_vectorstore(
            chunks
        )

        repository_name = repo_url.rstrip("/").split("/")[-1]

        return {
            "status": "success",
            "repository": repository_name,
            "documents_processed": len(documents),
            "chunks_created": len(chunks),
        }