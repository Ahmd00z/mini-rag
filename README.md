# mini-rag

This is a minimal implementation of the RAG model for question answering.

## Description

**mini-rag** is a full, production-style implementation of a **Retrieval-Augmented
Generation (RAG)** pipeline — a system that lets you upload your own documents,
process them, and ask natural-language questions that get answered using the
content of those documents instead of relying solely on an LLM's built-in
knowledge.

The project is intentionally built in layers, each one solving a real problem
you'd face moving from a prototype to a production system. Below is a breakdown
of what's inside and why it's there.

### How RAG works in this project

1. **Upload** a document (PDF, TXT) to a project.
2. **Process**: the document is split into smaller, overlapping text **chunks**.
3. **Embed**: each chunk is converted into a vector (embedding) using an
   embedding model, and stored in a vector database.
4. **Ask**: when a question comes in, it's embedded too, and the most similar
   chunks are retrieved from the vector database.
5. **Generate**: those chunks are passed as context to an LLM, which generates
   a grounded answer based only on the retrieved content.

### Core architecture

- **FastAPI**: the main web framework exposing REST endpoints for uploading
  files, triggering processing, and asking questions.
- **PostgreSQL + SQLAlchemy + Alembic**: relational storage for projects,
  assets, and chunks, with foreign-key integrity and versioned schema
  migrations instead of manual database changes.
- **Vector Search — pluggable backend**:
  - **Qdrant**: a dedicated, high-performance vector database.
  - **pgvector**: vector storage directly inside PostgreSQL, for simpler
    deployments that don't need a separate vector DB.
- **LLM Providers — pluggable backend**: a factory pattern lets you switch
  between generation/embedding providers without touching business logic:
  - OpenAI
  - Cohere
  - Google Gemini
  - Local models via Ollama (through an OpenAI-compatible endpoint)
- **Background Processing — Celery + RabbitMQ + Redis**: file processing and
  indexing run asynchronously as background tasks instead of blocking API
  requests, with automatic retries and task tracking.
  - **Flower**: a web dashboard to monitor Celery tasks and workers in
    real time.
  - **Celery Beat**: scheduled/periodic maintenance tasks.

### Production & deployment

- **Docker Compose**: the entire stack (API, database, vector DB, broker,
  monitoring) runs as a set of containerized services.
- **Nginx**: a reverse proxy in front of the API, handling routing and
  acting as the single public entry point.
- **Monitoring — Prometheus + Grafana**: request counts, latency, and system
  resource usage (CPU/RAM/disk) are collected and visualized on dashboards.
  - `node-exporter` for host-level system metrics.
  - `postgres-exporter` for database-level metrics.
- **CI/CD — GitHub Actions + systemd**: pushing to the deployment branch
  automatically pulls the latest code on the server and restarts the
  service via a systemd unit, which also ensures the app restarts
  automatically after a server reboot or crash.

### Key features

- Multiple **projects**, each with its own isolated set of files and
  vector collection.
- Configurable **chunk size** and **overlap** per processing request.
- A `do_reset` option to wipe and re-index a project's data cleanly.
- Swappable LLM/embedding/vector-DB backends via environment variables —
  no code changes required to switch providers.
- Multi-language prompt templates (Arabic/English) for generation.
- Batch embedding calls to reduce API overhead and latency.
- Health checks across services (database, broker, cache) to avoid
  race conditions on startup.

### Who this project is for

This repo is meant as a **learning resource** as much as a usable template:
it's built incrementally, tutorial by tutorial, so each piece of
infrastructure (relational modeling, vector search, provider abstraction,
observability, async task queues) can be understood on its own before being
combined into the full system. It's a good reference if you want to see how
a RAG project evolves from a simple local script into something closer to a
real, deployable backend service.

### Tech stack summary

| Layer | Technology |
|---|---|
| API | FastAPI |
| Database | PostgreSQL (SQLAlchemy + Alembic) |
| Vector Search | Qdrant / pgvector |
| LLM Providers | OpenAI, Cohere, Gemini, Ollama |
| Task Queue | Celery + RabbitMQ + Redis |
| Monitoring | Prometheus + Grafana |
| Reverse Proxy | Nginx |
| Deployment | Docker Compose, GitHub Actions, systemd |

## Requirements

- Python 3.10

#### Install Dependencies

```bash
sudo apt update
sudo apt install libpq-dev gcc python3-dev
```

#### Install Python using MiniConda

1) Download and install MiniConda from [here](https://docs.anaconda.com/free/miniconda/#quick-command-line-install)
2) Create a new environment using the following command:
```bash
$ conda create -n mini-rag python=3.10
```
3) Activate the environment:
```bash
$ conda activate mini-rag
```

### (Optional) Setup you command line interface for better readability

```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

### (Optional) Run Ollama Local LLM Server using Colab + Ngrok

- Check the [notebook](https://colab.research.google.com/drive/1KNi3-9KtP-k-93T3wRcmRe37mRmGhL9p?usp=sharing) + [Video](https://youtu.be/-epZ1hAAtrs)

## Installation

### Install the required packages

```bash
$ pip install -r requirements.txt
```

### Setup the environment variables

```bash
$ cp .env.example .env
```

### Run Alembic Migration

```bash
$ alembic upgrade head
```

Set your environment variables in the `.env` file. Like `OPENAI_API_KEY` value.

## Run Docker Compose Services

```bash
$ cd docker
$ cp .env.example .env
```

- update `.env` with your credentials



```bash
$ cd docker
$ sudo docker compose up -d
```

## Access Services

- **FastAPI**: http://localhost:8000
- **Flower Dashboard**: http://localhost:5555 (admin/password from env)
- **Grafana**: http://localhost:3000
- **Prometheus**: http://localhost:9090

## Run the FastAPI server (Development Mode)

```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

# Celery (Development Mode)

For development, you can run Celery services manually instead of using Docker:

To Run the **Celery worker**, you need to run the following command in a separate terminal:

```bash
$ python -m celery -A celery_app worker --queues=default,file_processing,data_indexing --loglevel=info
```

To run the **Beat scheduler**, you can run the following command in a separate terminal:

```bash
$ python -m celery -A celery_app beat --loglevel=info
```

To Run **Flower Dashboard**, you can run the following command in a separate terminal:

```bash
$ python -m celery -A celery_app flower --conf=flowerconfig.py
```


open your browser and go to `http://localhost:5555` to see the dashboard.

## POSTMAN Collection

Download the POSTMAN collection from [/assets/mini-rag-app.postman_collection.json](/assets/mini-rag-app.postman_collection.json)
