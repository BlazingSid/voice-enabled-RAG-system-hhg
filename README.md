# 🎙️ VoiceRAG

A voice-enabled Retrieval-Augmented Generation (RAG) system built for **HH Goa 2026 — Task 2**.

The system allows a user to speak a question, converts the speech into text, retrieves relevant information from the provided dataset, and generates a grounded answer.

## 🚀 Pipeline

```text
Voice Input
    ↓
Speech-to-Text
    ↓
Query Processing
    ↓
Chunking / Retrieval
    ↓
Vector Database
    ↓
Context Selection
    ↓
LLM / Answer Generation
    ↓
Guardrails
    ↓
Final Answer
```

## 🎯 Goal

Build a fast and reliable voice-enabled RAG pipeline that:

* Accepts voice questions
* Transcribes speech into text
* Retrieves relevant context from the dataset
* Generates answers grounded in retrieved context
* Handles off-topic and unsafe queries
* Detects when the system does not have enough information
* Measures and optimizes end-to-end latency

The target is **under 200ms** for the complete pipeline.

## 📚 Dataset

The project uses the **MSMARCO-XI** dataset provided for the challenge.

Dataset:
https://huggingface.co/datasets/ai4bharat/MSMARCO-XI

## 🧠 Core Components

### 1. Speech-to-Text

Using one of:

* Sarvam
* ElevenLabs

The final choice will be documented here.

### 2. Intelligent Chunking

Instead of relying on a single fixed-size chunking strategy, the system will experiment with multiple approaches such as:

* Fixed-size chunks
* Overlapping chunks
* Semantic chunking
* Metadata-aware chunking

The goal is to determine which strategy provides the best retrieval quality and latency.

### 3. Retrieval

Relevant chunks are indexed inside a vector database and retrieved for each user query.

### 4. Generation

The retrieved context is passed to the generation model to produce an answer grounded in the available information.

### 5. Model Harness

The model will run through a structured orchestration layer handling:

* Input validation
* Tool/model calls
* Retries
* Structured outputs
* Error recovery
* Pipeline state

This avoids relying on a single raw prompt → response call.

### 6. Guardrails

The system should know when **not** to answer.

Guardrails will handle:

* Off-topic questions
* Unsafe/inappropriate inputs
* Unsupported questions
* Hallucination detection
* Insufficient retrieved context

Answers should be grounded in retrieved information.

## ⚡ Performance

Target:

**< 200ms end-to-end latency**

We will benchmark the pipeline across multiple test queries and report:

| Metric | Result |
| ------ | -----: |
| P50    |    TBD |
| P70    |    TBD |
| P100   |    TBD |

The benchmark will use a reasonable number of queries rather than a single best-case run.

## 🏗️ Project Structure

```text
voicerag/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── rag/
│   ├── services/
│   ├── guardrails/
│   └── main.py
│
├── data/
│   └── .gitkeep
│
├── scripts/
│   ├── ingest.py
│   └── benchmark.py
│
├── tests/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 🛠️ Tech Stack

**Backend**

* Python
* FastAPI

**Speech-to-Text**

* Sarvam / ElevenLabs

**RAG**

* TBD

**Vector Database**

* TBD

**LLM**

* TBD

**Evaluation**

* Custom latency benchmarking
* Retrieval evaluation

## 📈 Development Plan

[✓] Learned RAG architecture
[✓] Learned embeddings
[✓] Created FastAPI backend
[✓] Created project structure
[✓] Added health endpoint
[✓] Added structured request/response schemas
[✓] Created RAG orchestrator skeleton

[ ] Connect dataset
[ ] Implement vector database
[ ] Implement retrieval
[ ] Add LLM
[ ] Add STT
[ ] Add guardrails
[ ] Add retries/error handling
[ ] Benchmark latency
[ ] Integrate frontend

## 👥 Team

Built for **HH Goa 2026**.

Team: **Synrox**

## 📅 Challenge

**HH Goa 2026 — Task 2: Build a Voice-Enabled RAG Model**

Task launched: **August 13, 2026**

Deadline: **August 22, 2026 — 11:59 PM**

## 📢 Hashtag

`#RAGInGoa`
