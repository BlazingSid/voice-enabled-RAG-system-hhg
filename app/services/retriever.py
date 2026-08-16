from typing import Protocol


class Retriever(Protocol):
    async def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:
        ...