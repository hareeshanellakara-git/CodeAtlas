from pathlib import Path

from langchain_community.vectorstores import FAISS

from backend.config import settings
from backend.services.embedding_service import EmbeddingService


class VectorStoreService:

    def __init__(self):

        self.embedding_model = (
            EmbeddingService()
            .get_embedding_model()
        )

        self.vectorstore_path = Path(
            settings.VECTORSTORE_PATH
        )

    def create_vectorstore(self, documents):

        vectorstore = FAISS.from_documents(
            documents=documents,
            embedding=self.embedding_model,
        )

        self.vectorstore_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        vectorstore.save_local(
            str(self.vectorstore_path)
        )

        return vectorstore

    def load_vectorstore(self):

        return FAISS.load_local(
            str(self.vectorstore_path),
            self.embedding_model,
            allow_dangerous_deserialization=True,
        )