📚 Retrieval-Augmented Generation (RAG) Flask Application

This project is a production-ready Retrieval-Augmented Generation (RAG) system built from a research notebook and deployed as a Flask web application with a simple UI.

It combines:

Semantic retrieval (FAISS + Sentence Transformers)

Grounded answer generation with citations

Confidence-aware guardrails

Wikipedia + local document sources

UI served via Flask

Extensible self-learning foundation

🚀 Features

🔎 Chunk-level semantic retrieval using FAISS

🧠 Sentence-level grounding (answers must come from retrieved context)

🛡 Guardrails to avoid vague or speculative answers

📌 Citations with retrieval scores & similarity

📊 Confidence estimation based on retrieval strength

🌐 Wikipedia + local documents as knowledge sources

🖥 Web UI for interactive querying

🔁 Designed for future self-learning (feedback, memory, retraining)



rag_app/
│
├── app.py                    # Flask application entry point
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
│
├── Documents/                # Local knowledge base
│   ├── doc1.txt
│   ├── doc2.txt
│   └── doc3.txt
│
├── ui/                       # Frontend UI
│   ├── index.html
│   ├── style.css
│   └── script.js
│
└── rag/                      # Core RAG logic (modularized from notebook)
    ├── __init__.py
    ├── ingestion.py          # Document loading, chunking, FAISS index
    ├── pipeline.py           # RAG pipeline (retrieval → grounding → citation)
    ├── models.py             # Embedding model
    └── confidence.py         # Confidence computation





🧠 RAG Pipeline Overview

The system follows this flow:

User Query
   ↓
Guarded Semantic Retrieval (FAISS)
   ↓
Chunk Filtering (confidence threshold)
   ↓
Context Sentence Extraction
   ↓
Sentence-Level Similarity Scoring
   ↓
Guardrail Filtering
   ↓
Grounded Answer + Citation
   ↓
Confidence Score


Only answers grounded in retrieved content are returned.

🔍 Knowledge Sources
1. Local Documents

Text files placed in the Documents/ directory:

doc1.txt

doc2.txt

doc3.txt

Each document is:

Split into sentence chunks

Embedded

Indexed in FAISS

Used for citation and grounding

2. Wikipedia

Automatically ingested summaries from:

Football

Association football

🧩 Guardrails & Confidence
Guarded Retrieval

Uses cosine similarity

Filters chunks below a minimum score (MIN_SCORE = 0.45)

If no chunk passes → no answer is generated

Sentence Guardrail

Prevents vague answers by rejecting sentences containing:

usually, between, include, some, variations

Confidence Score

Computed as the mean retrieval score of the accepted chunks.

🌐 Web Interface

Served via Flask

Simple HTML/CSS/JS frontend

Displays:

Answer

Confidence

Retrieved evidence chunks

Source (Wikipedia or document)

⚙ Installation & Setup
1️⃣ Install Dependencies
pip install -r requirements.txt

2️⃣ Run the Application
python app.py

3️⃣ Open in Browser
http://127.0.0.1:5000

📦 Requirements
flask
faiss-cpu
sentence-transformers
wikipedia
numpy
torch
transformers
regex

🔁 Notebook → App Migration

This project was originally developed as a research notebook and later:

Modularized into clean Python files

Preserved exact RAG logic

Converted into a Flask API

Connected to a browser-based UI

No core algorithmic logic was changed during migration.

🔮 Future Extensions (Planned)

👍👎 User feedback integration

🧠 Self-learning memory (query reformulation, KB expansion)

🔄 Periodic retraining from interaction logs

📊 Analytics dashboard

🐳 Docker deployment

☁ Cloud hosting
