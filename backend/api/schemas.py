from pydantic import BaseModel, HttpUrl


class IngestRequest(BaseModel):

    repository_url: HttpUrl


class IngestResponse(BaseModel):

    message: str


class ChatRequest(BaseModel):

    question: str


class ChatResponse(BaseModel):

    answer: str
    sources: list[str]