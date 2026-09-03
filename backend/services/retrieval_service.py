from langchain_core.documents import Document

from backend.services.vectorstore_service import VectorStoreService


class RetrievalService:

    def __init__(self):

        self.vectorstore = (
            VectorStoreService()
            .load_vectorstore()
        )

    def retrieve_with_scores(
        self,
        question: str,
        k: int = 6,
    ) -> list[tuple[Document, float]]:

        # Retrieve more candidates than we finally expose.
        # This gives the ranking layer more evidence to work with.
        candidate_results = (
            self.vectorstore
            .similarity_search_with_relevance_scores(
                question,
                k=8,
            )
        )

        # Rank the retrieved chunks by relevance.
        ranked_results = sorted(
            candidate_results,
            key=lambda item: item[1],
            reverse=True,
        )

        # Return the top 6 chunks.
        return ranked_results[:k]