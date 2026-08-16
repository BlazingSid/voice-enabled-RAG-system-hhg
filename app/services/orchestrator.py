from app.services.llm import LLM
from app.services.retriever import Retriever


class RAGOrchestrator:

    def __init__(
        self,
        retriever: Retriever,
        llm: LLM,
    ):
        self.retriever = retriever
        self.llm = llm

    async def run(self, query: str) -> dict:
        query = query.strip()

        if not query:
            raise ValueError("Query cannot be empty.")

        context = await self.retriever.search(
            query,
            top_k=5,
        )

        answer = await self.llm.generate(
            query,
            context,
        )

        return {
            "answer": answer,
            "grounded": bool(context),
            "sources": context,
        }