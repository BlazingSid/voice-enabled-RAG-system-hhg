from fastapi import FastAPI
app = FastAPI(
    title="HH Goa Voice RAG",
    version="0.1.0"
)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "hhgoa-rag"
    }