from huggingface_hub import hf_hub_download
import pyarrow.parquet as pq
import json
import os

REPO_ID = "ai4bharat/MSMARCO-XI"
OUTPUT_FILE = "data/raw/marathi_sample.jsonl"

file_path = hf_hub_download(
    repo_id=REPO_ID,
    repo_type="dataset",
    filename="train/martrain.parquet",
)

print("Reading dataset...")

parquet_file = pq.ParquetFile(file_path)

os.makedirs("data/raw", exist_ok=True)

count = 0
TARGET = 10_000

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

    for batch in parquet_file.iter_batches(
        batch_size=1000
    ):
        rows = batch.to_pylist()

        for row in rows:

            f.write(
                json.dumps(row, ensure_ascii=False)
                + "\n"
            )

            count += 1

            if count >= TARGET:
                break

        print(f"Extracted: {count}/{TARGET}")

        if count >= TARGET:
            break

print(f"\nDone!")
print(f"Saved {count} samples to {OUTPUT_FILE}")