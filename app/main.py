from fastapi import FastAPI

from app.api.routes.query import router as query_router

app = FastAPI(
    title="HH Goa Voice RAG",
    version="0.1.0",
)

app.include_router(query_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "hhgoa-rag",
    }