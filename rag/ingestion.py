# rag/ingestion.py

import os
import re
import wikipedia
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# -----------------------------
# Config
# -----------------------------
DOCS_PATH = "Documents"
WIKI_PAGES = ["Football", "Association football"]
MIN_SCORE = 0.45
CHUNK_SIZE = 3   # sentences per chunk

# -----------------------------
# Model
# -----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# Global storage
# -----------------------------
index = None
all_chunks = []
metadata = []


# -----------------------------
# Helpers
# -----------------------------
def split_into_chunks(text, chunk_size=CHUNK_SIZE):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []

    for i in range(0, len(sentences), chunk_size):
        chunk = " ".join(sentences[i:i + chunk_size]).strip()
        if chunk:
            chunks.append(chunk)

    return chunks


# -----------------------------
# Load documents
# -----------------------------
def load_documents():
    docs = []

    # ---- Local documents ----
    for file in os.listdir(DOCS_PATH):
        if file.endswith(".txt"):
            with open(os.path.join(DOCS_PATH, file), "r", encoding="utf-8") as f:
                docs.append({
                    "text": f.read(),
                    "topic": file
                })

    # ---- Wikipedia ----
    for page in WIKI_PAGES:
        content = wikipedia.summary(page, sentences=8)
        docs.append({
            "text": content,
            "topic": "Wikipedia"
        })

    return docs


# -----------------------------
# Build FAISS index
# -----------------------------
def build_index():
    global index, all_chunks, metadata

    docs = load_documents()

    all_chunks = []
    metadata = []

    for doc in docs:
        chunks = split_into_chunks(doc["text"])
        for chunk in chunks:
            all_chunks.append(chunk)
            metadata.append(doc["topic"])

    embeddings = model.encode(all_chunks, show_progress_bar=True)

    # Normalize for cosine similarity
    faiss.normalize_L2(embeddings)

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)


# -----------------------------
# Retrieval
# -----------------------------
def retrieve_with_scores(query, top_k=10):
    global index

    if index is None:
        build_index()

    query_vec = model.encode([query])
    faiss.normalize_L2(query_vec)

    scores, indices = index.search(query_vec, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        results.append({
            "score": float(score),
            "text": all_chunks[idx],
            "topic": metadata[idx],
            "chunk_id": int(idx)
        })

    return results


def guarded_retrieval(query, top_k=10):
    results = retrieve_with_scores(query, top_k=top_k)
    results = [r for r in results if r["score"] >= MIN_SCORE]
    return results if results else None
