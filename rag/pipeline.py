# rag/pipeline.py

import re
import numpy as np
import faiss

from rag.ingestion import guarded_retrieval
from rag.models import model   # sentence-transformers model
from rag.confidence import compute_confidence


# -----------------------------
# Guardrail
# -----------------------------
def generic_sentence_guardrail(sentence):
    bad_terms = ["usually", "between", "include", "some", "variations"]
    return not any(t in sentence.lower() for t in bad_terms)


# -----------------------------
# Context builder
# -----------------------------
def build_context_with_sources(results, max_chunks=3):
    context_sentences = []
    sources = []

    for r in results[:max_chunks]:
        sentences = re.split(r'(?<=[.!?])\s+', r["text"])
        for s in sentences:
            s = s.strip()
            if not s:
                continue

            context_sentences.append(s)
            sources.append({
                "topic": r["topic"],
                "retrieval_score": round(r["score"], 3),
                "chunk_id": r["chunk_id"],
                "chunk": r["text"]
            })

    return context_sentences, sources


# -----------------------------
# Answer generation with citation
# -----------------------------
def generate_answer_with_citation(query, context_sentences, sources, min_sim=0.65):
    if not context_sentences:
        return None, None

    query_emb = model.encode([query])
    sent_embs = model.encode(context_sentences)

    faiss.normalize_L2(query_emb)
    faiss.normalize_L2(sent_embs)

    sims = np.dot(sent_embs, query_emb.T).squeeze()
    ranked = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)

    for idx, sim in ranked:
        sent = context_sentences[idx]
        if sim >= min_sim and generic_sentence_guardrail(sent):
            citation = sources[idx]
            citation["sentence_similarity"] = round(float(sim), 3)
            return sent, citation

    return "I cannot answer this question using the provided context.", None


# -----------------------------
# MAIN RAG PIPELINE (Notebook-accurate)
# -----------------------------
def rag_pipeline(query, top_k=10, max_chunks=3):
    results = guarded_retrieval(query, top_k=top_k)

    if results is None:
        return {
            "answer": None,
            "confidence": 0.0,
            "citations": None,
            "status": "Low retrieval confidence"
        }

    context_sentences, sources = build_context_with_sources(
        results, max_chunks
    )

    answer, citation = generate_answer_with_citation(
        query, context_sentences, sources
    )

    if citation is None:
        return {
            "answer": answer,
            "confidence": 0.0,
            "citations": None,
            "status": "No grounded answer found"
        }

    return {
        "answer": answer,
        "confidence": compute_confidence(results),
        "citations": [citation],
        "status": "OK"
    }