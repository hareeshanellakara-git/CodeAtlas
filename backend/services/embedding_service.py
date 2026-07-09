from langchain_huggingface import HuggingFaceEmbeddings

from backend.config import settings


class EmbeddingService:
    

    def __init__(self):

        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            model_kwargs={
                "device": "cpu"
            },
            encode_kwargs={
                "normalize_embeddings": True
            },
        )

    def get_embedding_model(self) -> HuggingFaceEmbeddings:
        return self.embeddings