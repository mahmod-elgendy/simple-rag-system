async function askQuestion() {
    const q = document.getElementById("question").value;

    const res = await fetch("/ask", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ query: q })
    });

    const data = await res.json();

    document.getElementById("answer").innerText =
        `${data.answer}\n\nConfidence: ${data.confidence}`;

    let chunksDiv = document.getElementById("chunks");
    chunksDiv.innerHTML = "";

    if (data.citations) {
        data.citations.forEach(c => {
            let p = document.createElement("p");
            p.innerText = `[${c.topic}] ${c.chunk}`;
            chunksDiv.appendChild(p);
        });
    }
}
