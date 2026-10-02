const message = document.getElementById("message");
const results = document.getElementById("results");
const errorBox = document.getElementById("error");

document.getElementById("sampleBtn").onclick = () => {
  message.value = "If you really cared about me, you would answer me right now. After everything I've done for you, you clearly don't care. This is your fault, and you'll regret ignoring me. You have to answer immediately.";
};

document.getElementById("clearBtn").onclick = () => {
  message.value = "";
  results.classList.add("hidden");
  errorBox.textContent = "";
};

document.getElementById("analyzeBtn").onclick = async () => {
  errorBox.textContent = "";
  const text = message.value.trim();
  if (!text) {
    errorBox.textContent = "Please enter a message first.";
    return;
  }

  const response = await fetch("/analyze", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({text})
  });

  const data = await response.json();
  if (!response.ok) {
    errorBox.textContent = data.error || "Something went wrong.";
    return;
  }

  document.getElementById("score").textContent = data.risk_score + "/100";
  document.getElementById("level").textContent = data.risk_level + " Risk";
  document.getElementById("description").textContent = data.description;
  document.getElementById("sentiment").textContent = data.sentiment.label;

  const patterns = document.getElementById("patterns");
  patterns.innerHTML = data.patterns.length ? data.patterns.map(p => `
    <div class="pattern">
      <strong>${p.category}</strong>
      <span>${p.count} matching pattern(s)</span>
      <div>${p.examples.map(e => `<span class="tag">${escapeHtml(e)}</span>`).join("")}</div>
    </div>
  `).join("") : "<p>No predefined manipulation patterns detected.</p>";

  document.getElementById("sentences").innerHTML = data.sentences.map(s => `
    <div class="sentence ${s.flagged ? "flagged" : ""}">
      ${escapeHtml(s.sentence)}
      ${s.flagged ? `<small>Flagged: ${s.categories.join(", ")}</small>` : ""}
    </div>
  `).join("");

  document.getElementById("recommendations").innerHTML =
    data.recommendations.map(r => `<li>${escapeHtml(r)}</li>`).join("");

  document.getElementById("disclaimer").textContent = data.disclaimer;
  results.classList.remove("hidden");
  results.scrollIntoView({behavior:"smooth"});
};

function escapeHtml(value) {
  return value.replace(/[&<>"']/g, c => ({
    "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"
  }[c]));
}
