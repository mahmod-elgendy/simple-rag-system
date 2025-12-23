# 📚 Retrieval-Augmented Generation (RAG) Flask Application

This project is a **production-ready Retrieval-Augmented Generation (RAG) system** originally developed in a research notebook and then **fully migrated into a Flask web application** with a browser-based UI.

The system focuses on **grounded, citation-backed answers** using semantic retrieval over **local documents and Wikipedia**, with strong guardrails and confidence estimation.

---

## 🚀 Key Features

- 🔎 **Semantic Retrieval** using FAISS + Sentence Transformers
- 🧠 **Sentence-level grounding** (answers must come from retrieved evidence)
- 🛡 **Guardrails** to avoid vague or speculative answers
- 📌 **Explicit citations** with retrieval & similarity scores
- 📊 **Confidence scoring** based on retrieval strength
- 🌐 **Hybrid knowledge base** (Local Documents + Wikipedia)
- 🖥 **Flask-powered Web UI**
- 🔁 **Designed for future self-learning** (feedback, memory, retraining)

---

## 🗂 Project Structure

rag_app/
│
├── app.py # Flask application entry point
├── requirements.txt # Python dependencies
├── README.md # Project documentation
│
├── Documents/ # Local knowledge base
│ ├── doc1.txt
│ ├── doc2.txt
│ └── doc3.txt
│
├── ui/ # Frontend UI
│ ├── index.html
│ ├── style.css
│ └── script.js
│
└── rag/ # Core RAG logic (from notebook)
├── init.py
├── ingestion.py # Document ingestion, chunking, FAISS index
├── pipeline.py # RAG pipeline (retrieval → grounding → citation)
├── models.py # Embedding model loader
└── confidence.py # Confidence computation


---

## 🧠 RAG Pipeline Overview

The system follows a **strict grounded-answer pipeline**:
User Query
↓
Guarded Semantic Retrieval (FAISS)
↓
Chunk Filtering (confidence threshold)
↓
Sentence Extraction from Chunks
↓
Sentence–Query Similarity Scoring
↓
Guardrail Filtering
↓
Grounded Answer + Citation
↓
Confidence Score


If **no reliable evidence** is found, the system refuses to hallucinate.

---

## 🔍 Knowledge Sources

### 📄 Local Documents
- Stored in the `Documents/` folder
- Each `.txt` file is:
  - Sentence-split
  - Chunked
  - Embedded
  - Indexed
  - Used as a citable source

### 🌐 Wikipedia
Automatically ingested summaries from:
- **Football**
- **Association football**

Wikipedia content is treated the same as local documents and fully citable.

---

## 🧩 Guardrails & Confidence

### 🔐 Guarded Retrieval
- Uses cosine similarity (FAISS Inner Product)
- Filters chunks below a minimum similarity score (`MIN_SCORE = 0.45`)
- If no chunk passes → no grounded answer is returned

### 🚫 Sentence Guardrail
Rejects vague or non-factual sentences containing:


### 📊 Confidence Score
Computed as the **mean similarity score** of the retrieved chunks used to answer the query.

---

## 🌐 Web Interface

- Built with **HTML + CSS + JavaScript**
- Served directly by Flask
- Displays:
  - Final Answer
  - Confidence Score
  - Evidence Chunks
  - Source (Wikipedia or document)

The UI communicates with the backend via a `/ask` JSON API.

---

## ⚙ Installation & Setup

### 1️⃣ Install Dependencies

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

🔁 Notebook → Application Migration

This project was originally developed as a Jupyter notebook and later:

Modularized into clean Python modules

Preserved the exact RAG logic

Converted into a Flask API

Connected to a browser-based UI

Kept notebook behavior intact (no algorithmic changes)

🔮 Planned Extensions

👍👎 User feedback collection

🧠 Self-learning memory (query reformulation)

📚 Knowledge base expansion from high-confidence answers

🔄 Periodic retraining

📊 Analytics dashboard

🐳 Dockerization

☁ Cloud deployment

🧑‍💻 Design Philosophy

This system prioritizes:

Correctness over fluency

Grounded answers over hallucinations

Explainability through citations

Research-grade rigor with production readiness




