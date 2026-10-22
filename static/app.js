const expr = document.getElementById("expr");
const out = document.getElementById("out");
const historyEl = document.getElementById("history");
const angleBtn = document.getElementById("angle");
let angle = "rad";
let lastResult = "";
const history = [];

function insert(text) {
  const s = expr.selectionStart ?? expr.value.length;
  const e = expr.selectionEnd ?? expr.value.length;
  expr.value = expr.value.slice(0, s) + text + expr.value.slice(e);
  expr.focus();
  expr.setSelectionRange(s + text.length, s + text.length);
}

function renderHistory() {
  historyEl.replaceChildren();
  history.forEach((h) => {
    const li = document.createElement("li");
    const b = document.createElement("button");
    b.textContent = `${h.expression} = ${h.result}`; // textContent : pas de XSS
    b.addEventListener("click", () => { expr.value = h.expression; expr.focus(); });
    li.appendChild(b);
    historyEl.appendChild(li);
  });
}

async function evaluate() {
  const expression = expr.value.trim();
  if (!expression) return;
  try {
    const r = await fetch("/api/evaluate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ expression, angle }),
    });
    const data = await r.json();
    if (r.ok) {
      out.className = "";
      out.textContent = "= " + data.result;
      lastResult = String(data.result);
      history.unshift({ expression, result: data.result });
      if (history.length > 10) history.pop();
      renderHistory();
    } else {
      out.className = "err";
      out.textContent = data.error;
    }
  } catch (err) {
    out.className = "err";
    out.textContent = "Erreur réseau";
  }
}

document.querySelector(".grid").addEventListener("click", (ev) => {
  const btn = ev.target.closest("button");
  if (!btn) return;
  if (btn.dataset.ins) return insert(btn.dataset.ins);
  switch (btn.dataset.act) {
    case "clear": expr.value = ""; out.textContent = "\u00a0"; out.className = ""; break;
    case "back": expr.value = expr.value.slice(0, -1); break;
    case "ans": insert(lastResult); break;
    case "eval": evaluate(); break;
    case "angle":
      angle = angle === "rad" ? "deg" : "rad";
      angleBtn.textContent = angle.toUpperCase();
      break;
  }
});
expr.addEventListener("keydown", (ev) => { if (ev.key === "Enter") evaluate(); });
