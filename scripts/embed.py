"""
Generate embeddings for VoiceRAG chunks.
"""

from __future__ import annotations

import json

import numpy as np
from sentence_transformers import SentenceTransformer

from app.core.config import settings


def load_chunks() -> list[dict]:
    chunks = []

    with settings.CHUNKS_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                chunks.append(json.loads(line))

    return chunks


def main() -> None:
    chunks = load_chunks()

    print(f"Loaded chunks: {len(chunks):,}")
    print(f"Loading model: {settings.EMBEDDING_MODEL}")

    model = SentenceTransformer(
        settings.EMBEDDING_MODEL,
        device=settings.DEVICE,
    )

    texts = [chunk["text"] for chunk in chunks]

    print("Generating embeddings...")

    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    embeddings = np.asarray(embeddings, dtype=np.float32)

    output_path = settings.PROCESSED_DIR / "embeddings.npy"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    np.save(output_path, embeddings)

    print("\nEmbedding generation complete.")
    print(f"Shape: {embeddings.shape}")
    print(f"Dimension: {embeddings.shape[1]}")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()