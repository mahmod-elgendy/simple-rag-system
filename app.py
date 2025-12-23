from flask import Flask, request, jsonify, send_from_directory
from rag.pipeline import rag_pipeline

app = Flask(__name__, static_folder="ui")

# ---------------------------
# Serve UI
# ---------------------------
@app.route("/")
def index():
    return send_from_directory("ui", "index.html")


@app.route("/ui/<path:path>")
def serve_ui_files(path):
    return send_from_directory("ui", path)


# ---------------------------
# RAG API
# ---------------------------
@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "Empty query"}), 400

    # ---- Run RAG ----
    out = rag_pipeline(query)

    response = {
        "answer": out["answer"],
        "confidence": out["confidence"],
        "status": out["status"],
        "citations": out.get("citations", [])
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
