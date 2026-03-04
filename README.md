# DocIntel

**RAG-powered document intelligence tool.** Upload a PDF, ask questions in natural language, get accurate answers with citations showing exactly which page and section the answer came from.

🔗 **Live Demo:** [docintel-jv9v.onrender.com](https://docintel-jv9v.onrender.com)

---

## What It Does

1. **Upload a PDF** — the document is loaded, split into chunks, and embedded as vectors into a PostgreSQL database
2. **Ask a question** — your query is converted to a vector and semantically searched against stored chunks
3. **Get a cited answer** — GPT-4o-mini generates a grounded response with numbered citations linking back to exact pages in your document

---

## Tech Stack

| Layer | Technology |
|---|---|
| RAG Framework | LangChain |
| LLM + Embeddings | OpenAI (GPT-4o-mini + text-embedding-ada-002) |
| Vector Database | PostgreSQL + pgvector (Supabase) |
| Backend | FastAPI |
| Frontend | Jinja2 + HTML/CSS/JS |
| Containerization | Docker |
| Deployment | Render |

---

## Architecture

```
PDF Upload
    │
    ▼
PyPDFLoader → RecursiveCharacterTextSplitter (500 chars, 50 overlap)
    │
    ▼
OpenAIEmbeddings → PGVector (Supabase)
    │
    ▼
User Query → Embedding → Similarity Search (top 5 chunks)
    │
    ▼
GPT-4o-mini (temperature=0, grounded to context only)
    │
    ▼
Answer + Citations [1][2][3] with page numbers
```

---

## Key Design Decisions

- **Chunking with overlap** — 50-character overlap between chunks prevents meaning loss at boundaries
- **Grounded generation** — prompt instructs GPT to use ONLY retrieved context, preventing hallucination
- **Temperature 0** — deterministic answers for consistent, factual document Q&A
- **Embedding consistency** — identical model used in both ingestion and retrieval to ensure vector comparability
- **Metadata tagging** — each chunk stores document name and page number for citation tracing

---

## Running Locally

**Prerequisites:** Python 3.11+, Docker

```bash
# Clone the repo
git clone https://github.com/Sayid-ali-dev/DocIntel.git
cd DocIntel

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your OPENAI_API_KEY and DATABASE_URL

# Start PostgreSQL with pgvector
docker-compose up -d

# Run the app
uvicorn app.main:app --reload
```

Open [http://localhost:8000](http://localhost:8000)

---

## Project Structure

```
DocIntel/
├── app/
│   ├── main.py          # FastAPI endpoints (/upload, /ask)
│   ├── ingest.py        # PDF loading, chunking, embedding, storage
│   ├── retrieve.py      # Semantic search against vector store
│   ├── generate.py      # GPT answer generation with citations
│   └── templates/
│       └── index.html   # Frontend UI
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Related Projects

- **[StockSense](https://github.com/Sayid-ali-dev/StockSense)** — ML-powered stock prediction API using Random Forest with CI/CD pipeline
