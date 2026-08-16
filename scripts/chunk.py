"""
Create deterministic text chunks from ingested MSMARCO-XI passages.

Input:
    data/processed/raw_records.json

Output:
    data/processed/chunks.jsonl
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.core.config import settings


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Split text into overlapping word-based chunks."""
    words = text.split()

    if not words:
        return []

    if overlap >= chunk_size:
        raise ValueError("CHUNK_OVERLAP must be smaller than CHUNK_SIZE")

    chunks = []
    start = 0
    step = chunk_size - overlap

    while start < len(words):
        chunk_words = words[start : start + chunk_size]

        if not chunk_words:
            break

        chunks.append(" ".join(chunk_words))
        start += step

    return chunks


def load_records(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_chunks(records: list[dict]) -> list[dict]:
    chunks = []
    seen_passages: set[str] = set()
    chunk_id = 0

    for record in records:
        query_id = record["query_id"]

        for passage in record["passages"]:
            text = passage["text"].strip()

            if not text:
                continue

            # Deduplicate identical passages.
            normalized = " ".join(text.split()).lower()

            if normalized in seen_passages:
                continue

            seen_passages.add(normalized)

            passage_chunks = chunk_text(
                text,
                chunk_size=settings.CHUNK_SIZE,
                overlap=settings.CHUNK_OVERLAP,
            )

            for chunk_index, chunk in enumerate(passage_chunks):
                chunks.append(
                    {
                        "chunk_id": chunk_id,
                        "query_id": query_id,
                        "passage_id": passage["passage_id"],
                        "chunk_index": chunk_index,
                        "text": chunk,
                        "is_selected": passage["is_selected"],
                        "source_lang": record["source_lang"],
                        "target_lang": record["target_lang"],
                    }
                )

                chunk_id += 1

    return chunks


def save_chunks(chunks: list[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        type=Path,
        default=settings.PROCESSED_DIR / "raw_records.json",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=settings.CHUNKS_PATH,
    )

    args = parser.parse_args()

    records = load_records(args.input)

    print(f"Loaded records: {len(records):,}")

    chunks = build_chunks(records)

    save_chunks(chunks, args.output)

    print(f"Unique chunks created: {len(chunks):,}")
    print(f"Saved to: {args.output}")


if __name__ == "__main__":
    main()