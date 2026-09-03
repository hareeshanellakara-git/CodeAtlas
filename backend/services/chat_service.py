from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain,
)

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from backend.config import settings
from backend.services.retrieval_service import RetrievalService


class ChatService:

    def __init__(self):

        self.llm = ChatGroq(
            model=settings.LLM_MODEL,
            api_key=settings.GROQ_API_KEY,
            temperature=0,
        )

        self.retrieval_service = (
            RetrievalService()
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are CodeAtlas, an AI assistant that helps developers understand GitHub repositories.

Use ONLY the provided repository context to answer questions.

If the answer cannot be found in the retrieved context, reply:

"I couldn't find that information in this repository."

Keep answers concise, accurate, and technical when appropriate.

Context:
{context}
""",
                ),
                (
                    "human",
                    "{input}",
                ),
            ]
        )

        self.document_chain = (
            create_stuff_documents_chain(
                self.llm,
                self.prompt,
            )
        )

    def ask(
        self,
        question: str,
    ):

        retrieved_results = (
            self.retrieval_service
            .retrieve_with_scores(
                question,
                k=6,
            )
        )

        documents = [
            document
            for document, _ in retrieved_results
        ]

        result = self.document_chain.invoke(
            {
                "input": question,
                "context": documents,
            }
        )

        evidence = []

        for rank, (
            document,
            score,
        ) in enumerate(
            retrieved_results,
            start=1,
        ):

            source = document.metadata.get(
                "source",
                "Unknown file",
            )

            content = (
                document.page_content
                .strip()
            )

            preview = content[:300]

            if len(content) > 300:
                preview += "..."

            evidence.append(
                {
                    "rank": rank,
                    "source": source,
                    "score": round(
                        float(score),
                        4,
                    ),
                    "preview": preview,
                }
            )

        sources = list(
            dict.fromkeys(
                item["source"]
                for item in evidence
            )
        )

        return {
            "answer": result,
            "sources": sources,
            "evidence": evidence,
        }