from pydantic import BaseModel, HttpUrl


class IngestRequest(BaseModel):

    repository_url: HttpUrl
    


class IngestResponse(BaseModel):

    message: str
    
    repository: str

    documents_processed: int

    chunks_created: int

    embedding_model: str

    vector_database: str

    llm: str


class ChatRequest(BaseModel):

    question: str


class ChatResponse(BaseModel):

    answer: str
    sources: list[str]