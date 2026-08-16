class MockRetriever:
    async def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:
        return [
            {
                "text": "Temporary retrieved context for backend testing.",
                "score": 1.0,
                "metadata": {
                    "source": "mock",
                },
            }
        ]


class MockLLM:
    async def generate(
        self,
        query: str,
        context: list[dict],
    ) -> str:
        return f"Mock grounded answer for: {query}"