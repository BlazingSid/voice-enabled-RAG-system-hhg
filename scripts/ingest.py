"""
MSMARCO-XI ingestion pipeline.

Phase 1:
- Download/cache the Marathi training Parquet from Hugging Face.
- Read a limited number of records.
- Extract English passages and relevance labels.
- Save the extracted records locally.

This script intentionally does NOT generate embeddings or build a FAISS
index yet. Those are later stages of the pipeline.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pyarrow.parquet as pq
from huggingface_hub import hf_hub_download
from tqdm import tqdm

from app.core.config import settings


def download_dataset() -> Path:
    """Download the dataset once using Hugging Face's local cache."""
    print("Checking Hugging Face cache...")

    path = hf_hub_download(
        repo_id=settings.HF_REPO_ID,
        filename=settings.HF_FILENAME,
        repo_type="dataset",
    )

    print(f"Dataset available at: {path}")
    return Path(path)


def extract_records(parquet_path: Path, limit: int) -> list[dict]:
    """Extract a limited number of query/passage records."""
    parquet = pq.ParquetFile(parquet_path)

    print(f"Dataset rows: {parquet.metadata.num_rows:,}")
    print(f"Processing first {limit:,} rows...")

    records: list[dict] = []
    processed = 0

    for batch in parquet.iter_batches(
        batch_size=min(1000, limit),
        columns=[
            "source_lang",
            "target_lang",
            "query_id",
            "query",
            "Eng_Query",
            "passages",
        ],
    ):
        rows = batch.to_pylist()

        for row in tqdm(rows, desc="Extracting records", leave=False):
            if processed >= limit:
                break

            passages = row.get("passages") or {}

            english_passages = passages.get("English_passages") or []
            is_selected = passages.get("is_selected") or []

            extracted_passages = []

            for idx, text in enumerate(english_passages):
                if not text or not str(text).strip():
                    continue

                extracted_passages.append(
                    {
                        "passage_id": idx,
                        "text": str(text).strip(),
                        "is_selected": (
                            int(is_selected[idx])
                            if idx < len(is_selected)
                            else 0
                        ),
                    }
                )

            records.append(
                {
                    "query_id": row.get("query_id"),
                    "query": row.get("query"),
                    "english_query": row.get("Eng_Query"),
                    "source_lang": row.get("source_lang"),
                    "target_lang": row.get("target_lang"),
                    "passages": extracted_passages,
                }
            )

            processed += 1

        if processed >= limit:
            break

    return records


def save_records(records: list[dict], output_path: Path) -> None:
    """Save extracted records as JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(records):,} records to:")
    print(output_path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest a limited sample of MSMARCO-XI."
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Number of dataset records to process.",
    )

    args = parser.parse_args()

    if args.limit <= 0:
        raise ValueError("--limit must be greater than 0")

    dataset_path = download_dataset()

    output_path = settings.PROCESSED_DIR / "raw_records.json"

    records = extract_records(
        parquet_path=dataset_path,
        limit=args.limit,
    )

    save_records(records, output_path)

    print("\nIngestion stage complete.")
    print(f"Records processed: {len(records):,}")


if __name__ == "__main__":
    main()