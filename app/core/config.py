"""
VoiceRAG pipeline configuration.

All settings are loaded from environment variables with sensible defaults.
Place a .env file in the project root to override defaults locally.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Project root: two levels up from app/core/config.py
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Load .env from project root if it exists
load_dotenv(PROJECT_ROOT / ".env")


class Settings:
    """Central configuration for the VoiceRAG pipeline.

    Every setting can be overridden via an environment variable.
    """

    def __init__(self):
        # --- Paths ---
        self.DATA_DIR: Path = Path(
            os.getenv("DATA_DIR", str(PROJECT_ROOT / "data" / "raw"))
        )
        self.PROCESSED_DIR: Path = Path(
            os.getenv("PROCESSED_DIR", str(PROJECT_ROOT / "data" / "processed"))
        )

        # --- Embedding model ---
        self.EMBEDDING_MODEL: str = os.getenv(
            "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
        )
        self.DEVICE: str = os.getenv("DEVICE", "cpu")

        # --- Chunking (word-count approximation of tokens) ---
        self.CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "256"))
        self.CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "64"))

        # --- Retrieval ---
        self.TOP_K: int = int(os.getenv("TOP_K", "10"))

        # --- Dataset (centralised, not user-configurable via env) ---
        self.HF_REPO_ID: str = "ai4bharat/MSMARCO-XI"
        self.HF_FILENAME: str = "train/martrain.parquet"

        # --- Derived paths ---
        self.FAISS_INDEX_PATH: Path = self.PROCESSED_DIR / "faiss.index"
        self.CHUNKS_PATH: Path = self.PROCESSED_DIR / "chunks.jsonl"
        self.GROUND_TRUTH_PATH: Path = self.PROCESSED_DIR / "ground_truth.json"
        self.INGEST_META_PATH: Path = self.PROCESSED_DIR / "ingest_metadata.json"


# Singleton used across the project
settings = Settings()
