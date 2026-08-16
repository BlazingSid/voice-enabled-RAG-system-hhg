from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    query: str = Field(min_length=1)


class Source(BaseModel):
    text: str
    score: float | None = None
    metadata: dict = Field(default_factory=dict)


class QueryResponse(BaseModel):
    answer: str
    grounded: bool
    sources: list[Source] = Field(default_factory=list)