// app.js — Lógica de UI (fetch API, pintar tabla y KPIs)
const elTbody = document.getElementById("tbody-alumnos");
const elAsignados = document.getElementById("kpi-asignados");
const elTotal = document.getElementById("kpi-total");
const elCompleto = document.getElementById("kpi-completo");
const btnDistribuir = document.getElementById("btn-distribuir");
const btnReset = document.getElementById("btn-reset");

async function getStatus(){
  const res = await fetch("/api/status");
  return await res.json();
}

function render(state){
  elAsignados.textContent = state.asignados;
  elTotal.textContent = state.total;
  elCompleto.classList.toggle("hidden", !state.completo);
  btnDistribuir.disabled = state.completo;

  elTbody.innerHTML = "";
  state.items
    .sort((a,b)=> a.id - b.id)
    .forEach(item=>{
      const tr = document.createElement("tr");
      const tdId = document.createElement("td");
      tdId.className = "id";
      tdId.textContent = item.id;

      const tdNombre = document.createElement("td");
      tdNombre.className = "nombre";
      tdNombre.textContent = item.nombre;

      const tdLang = document.createElement("td");
      tdLang.className = "lang";
      tdLang.innerHTML = item.lenguaje
        ? `<span class="pill ok">${item.lenguaje}</span>`
        : `<span class="pill pending">—</span>`;

      tr.appendChild(tdId);
      tr.appendChild(tdNombre);
      tr.appendChild(tdLang);
      elTbody.appendChild(tr);
    });
}

async function distribuir(){
  btnDistribuir.disabled = true; // optimista
  const res = await fetch("/api/distribuir", { method: "POST" });
  const state = await res.json();
  render(state);
}

async function reset(){
  const ok = confirm("¿Seguro que quieres reiniciar las asignaciones?");
  if(!ok) return;
  const res = await fetch("/api/reset", { method: "POST" });
  const state = await res.json();
  render(state);
}

btnDistribuir.addEventListener("click", distribuir);
btnReset.addEventListener("click", reset);

// Init
getStatus().then(render);
