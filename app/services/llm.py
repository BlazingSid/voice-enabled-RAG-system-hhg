from typing import Protocol


class LLM(Protocol):
    async def generate(
        self,
        query: str,
        context: list[dict],
    ) -> str:
        ...