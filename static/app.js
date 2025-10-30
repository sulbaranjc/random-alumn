// app.js — Lógica de UI (fetch API, pintar grid de estudiantes y KPIs)
const elStudentsGrid = document.getElementById("students-grid");
const elAsignados = document.getElementById("kpi-asignados");
const elTotal = document.getElementById("kpi-total");
const elCompleto = document.getElementById("kpi-completo");
const btnDistribuir = document.getElementById("btn-distribuir");
const btnReset = document.getElementById("btn-reset");

async function getStatus() {
  const res = await fetch("/api/status");
  return await res.json();
}

function render(state) {
  elAsignados.textContent = state.asignados;
  elTotal.textContent = state.total;
  elCompleto.classList.toggle("hidden", !state.completo);
  btnDistribuir.disabled = state.completo;

  elStudentsGrid.innerHTML = "";
  state.items
    .sort((a, b) => a.id - b.id)
    .forEach(item => {
      const card = document.createElement("div");
      card.className = "student-card";

      const studentInfo = document.createElement("div");
      studentInfo.className = "student-info";

      const studentId = document.createElement("div");
      studentId.className = "student-id";
      studentId.textContent = item.id;

      const studentName = document.createElement("div");
      studentName.className = "student-name";
      studentName.textContent = item.nombre;

      const studentLanguage = document.createElement("div");
      studentLanguage.className = "student-language";
      studentLanguage.innerHTML = item.lenguaje
        ? `<span class="pill ok">${item.lenguaje}</span>`
        : `<span class="pill pending">—</span>`;

      studentInfo.appendChild(studentId);
      studentInfo.appendChild(studentName);
      card.appendChild(studentInfo);
      card.appendChild(studentLanguage);
      elStudentsGrid.appendChild(card);
    });
}

async function distribuir() {
  btnDistribuir.disabled = true; // optimista
  const res = await fetch("/api/distribuir", { method: "POST" });
  const state = await res.json();
  render(state);
}

async function reset() {
  const ok = confirm("¿Seguro que quieres reiniciar las asignaciones?");
  if (!ok) return;
  const res = await fetch("/api/reset", { method: "POST" });
  const state = await res.json();
  render(state);
}

btnDistribuir.addEventListener("click", distribuir);
btnReset.addEventListener("click", reset);

// Init
getStatus().then(render);
