from langchain_community.embeddings import FastEmbedEmbeddings


class EmbeddingService:

    def __init__(self):

        self.embeddings = FastEmbedEmbeddings(
            model_name="BAAI/bge-small-en-v1.5"
        )

    def get_embedding_model(self):

        return self.embeddings