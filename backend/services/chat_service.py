from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain,
)

from langchain_classic.chains import (
    create_retrieval_chain,
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

        self.retriever = (
            RetrievalService()
            .get_retriever()
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

        self.retrieval_chain = (
            create_retrieval_chain(
                self.retriever,
                self.document_chain,
            )
        )

    def ask(self, question: str):

        return self.retrieval_chain.invoke(
            {
                "input": question,
            }
        )