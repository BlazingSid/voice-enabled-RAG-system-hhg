from fastapi import APIRouter, HTTPException

from app.schemas.query import QueryRequest, QueryResponse
from app.services.mock_services import MockLLM, MockRetriever
from app.services.orchestrator import RAGOrchestrator


router = APIRouter(prefix="/query", tags=["query"])

orchestrator = RAGOrchestrator(
    retriever=MockRetriever(),
    llm=MockLLM(),
)


@router.post("", response_model=QueryResponse)
async def query(request: QueryRequest):
    try:
        result = await orchestrator.run(request.query)
        return QueryResponse(**result)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="RAG pipeline failed.",
        ) from exc