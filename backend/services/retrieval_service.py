from langchain_core.vectorstores import VectorStoreRetriever

from backend.services.vectorstore_service import VectorStoreService


class RetrievalService:

    def __init__(self):

        self.vectorstore = (
            VectorStoreService()
            .load_vectorstore()
        )

    def get_retriever(self) -> VectorStoreRetriever:

        return self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": 4,
            },
        )