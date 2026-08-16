"""
Build a FAISS cosine-similarity index from generated embeddings.
"""

from __future__ import annotations

import numpy as np
import faiss

from app.core.config import settings


def main() -> None:
    embeddings = np.load(
        settings.PROCESSED_DIR / "embeddings.npy"
    ).astype("float32")

    print(f"Loaded embeddings: {embeddings.shape}")

    dimension = embeddings.shape[1]

    # Embeddings were normalized during generation.
    # Inner product therefore corresponds to cosine similarity.
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    settings.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    faiss.write_index(
        index,
        str(settings.FAISS_INDEX_PATH),
    )

    print("FAISS index built successfully.")
    print(f"Vectors indexed: {index.ntotal:,}")
    print(f"Dimension: {dimension}")
    print(f"Saved to: {settings.FAISS_INDEX_PATH}")


if __name__ == "__main__":
    main()