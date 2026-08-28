(() => {
  "use strict";

  const result = document.getElementById("result");
  const expr = document.getElementById("expr");
  const sciPad = document.getElementById("sciPad");
  const modeBtn = document.getElementById("modeBtn");
  const backBtn = document.getElementById("backBtn");

  let current = "0", stored = "", op = null, fresh = false, sci = false;
  const sym = { "+": "+", "-": "−", "*": "×", "/": "÷", "^": "^" };

  function render() {
    result.textContent = current;
    result.classList.toggle("small", current.length > 10);
    result.classList.remove("error");
    expr.textContent = stored && op ? `${stored} ${sym[op]}` : "";
  }

  function err() {
    current = "Error"; result.classList.add("error");
    stored = ""; op = null; fresh = true;
  }

  function num(d) {
    if (fresh) { current = d; fresh = false; }
    else current = current === "0" ? d : current + d;
    render();
  }

  function dot() {
    if (fresh) { current = "0."; fresh = false; }
    else if (!current.includes(".")) current += ".";
    render();
  }

  function clearAll() { current = "0"; stored = ""; op = null; fresh = false; render(); }

  function sign() {
    if (current === "0") return;
    current = current.startsWith("-") ? current.slice(1) : "-" + current;
    render();
  }

  function pct() {
    const n = parseFloat(current);
    if (Number.isNaN(n)) return err();
    current = String(n / 100); render();
  }

  function back() {
    if (fresh) return;
    if (current.length <= 1 || (current.length === 2 && current.startsWith("-"))) current = "0";
    else current = current.slice(0, -1);
    render();
  }

  function setOp(o) {
    const n = parseFloat(current);
    if (Number.isNaN(n)) return err();
    if (op && !fresh) calc(false);
    stored = current; op = o; fresh = true; render();
  }

  function calc(final = true) {
    if (!op) return;
    const a = parseFloat(stored), b = parseFloat(current);
    if (Number.isNaN(a) || Number.isNaN(b)) return err();
    let out;
    switch (op) {
      case "+": out = a + b; break;
      case "-": out = a - b; break;
      case "*": out = a * b; break;
      case "/": if (b === 0) return err(); out = a / b; break;
      case "^": out = Math.pow(a, b); break;
      default: return;
    }
    if (!Number.isFinite(out)) return err();
    if (final) expr.textContent = `${stored} ${sym[op]} ${current} =`;
    current = String(Number(out.toPrecision(12)));
    op = null; stored = ""; fresh = true; render();
  }

  function fn(name) {
    const n = parseFloat(current);
    if (Number.isNaN(n)) return err();
    const r = n * Math.PI / 180;
    let out;
    if (name === "sin") out = Math.sin(r);
    else if (name === "cos") out = Math.cos(r);
    else if (name === "tan") out = Math.tan(r);
    else if (name === "log") out = Math.log10(n);
    else if (name === "sqrt") out = Math.sqrt(n);
    else return;
    if (!Number.isFinite(out)) return err();
    expr.textContent = `${name}(${current}) =`;
    current = String(Number(out.toPrecision(12)));
    fresh = true; render();
  }

  function constant(name) {
    const m = { pi: Math.PI, e: Math.E };
    if (!(name in m)) return;
    current = String(Number(m[name].toPrecision(12)));
    fresh = true; render();
  }

  function click(e) {
    const b = e.target.closest("button");
    if (!b) return;
    if (b.dataset.num) return num(b.dataset.num);
    if (b.dataset.op) return setOp(b.dataset.op);
    if (b.dataset.fn) return fn(b.dataset.fn);
    if (b.dataset.const) return constant(b.dataset.const);
    if (b.dataset.action === "clear") return clearAll();
    if (b.dataset.action === "sign") return sign();
    if (b.dataset.action === "percent") return pct();
    if (b.dataset.action === "dot") return dot();
    if (b.dataset.action === "equals") return calc(true);
  }

  function key(e) {
    if (/\d/.test(e.key)) num(e.key);
    else if (e.key === ".") dot();
    else if (e.key === "+") setOp("+");
    else if (e.key === "-") setOp("-");
    else if (e.key === "*") setOp("*");
    else if (e.key === "/") { e.preventDefault(); setOp("/"); }
    else if (e.key === "Enter" || e.key === "=") { e.preventDefault(); calc(true); }
    else if (e.key === "Escape") clearAll();
    else if (e.key === "Backspace") back();
    else if (e.key === "%") pct();
  }

  modeBtn.addEventListener("click", () => {
    sci = !sci;
    sciPad.classList.toggle("hidden", !sci);
    modeBtn.textContent = sci ? "Scientific" : "Standard";
  });

  document.querySelector(".keys").addEventListener("click", click);
  sciPad.addEventListener("click", click);
  backBtn.addEventListener("click", back);
  document.addEventListener("keydown", key);
  render();
})();
