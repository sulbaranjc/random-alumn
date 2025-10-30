# main.py — Monolito FastAPI con vista separada + estáticos (CSS/JS/Logo)
from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random

app = FastAPI()

# Montar estáticos y plantillas
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
#comentarios multilina
# ------- Datos base -------
alumnos_dam = {
    1: "FERNANDEZ DE GOMAR ANTONIO DAVID",
    2: "SÁNCHEZ RUFINO MARIO",
    3: "CRISTOBAL ROMÁN REBECA",
    4: "QUIROZ DE ZALDO ISRAEL",
    5: "BEN AYED ANIS",
    6: "MUÑOZ ESQUETA JAVIER",
    7: "BRICEÑO GUTIÉRREZ MÓNICA",
    8: "CORDOVA LAGUNA CARLOS SEBASTIAN",
    9: "DÍEZ CAÑETE IVÁN"
}
alumnos_daw = {
    1: "ALVARO ALONSO GONZALO",
    2: "HOXSAS QUIÑONES EDDY MARADONA",
    3: "GÓMEZ LALA DAVID STEVEN",
    4: "VALDÉS SILO DAVID",
    5: "REINA SÁNCHEZ SARA VANESSA",
    6: "CHAPARRO CABALLERO MARÍA",
    7: "BEECKMANS BARRIENTOS NICOLE BEATRIX",
    8: "ZAMORA TRILLO MARIA DE LOS ANGELES",
    9: "MARTIN RODRIGUEZ SERGIO JESUS",
    10: "CENDRERO GONZÁLEZ JUAN PEDRO",
    11: "REQUEJO DE LA CRUZ MARCO ANTHONY",
    12: "GÓMEZ MARTÍN MARCOS",
    13: "GARZON TORRES ALVARO IVAN",
    14: "PEREZ BRICEÑO PEDRO LORENZO",
    15: "ASCUY SALINAS GEORGE",
    16: "OLIVARES SOTO JOSELIN YASBEL",
    17: "GUTIERREZ SIVILA MANUEL IGNACIO"
}

#asignar los alumnos solo dam a la variable alumnos
# alumnos = alumnos_dam
alumnos = alumnos_daw

lenguajes_de_programacion = {
    1: "JavaScript",
    2: "PHP",
    3: "Java",
    4: "Python",
    5: "Ruby",
    6: "Kotlin",
    7: "Rust",
    8: "Dart",
    9: "C#",
    10: "JavaScript",
    11: "PHP",
    12: "Java",
    13: "Python",
    14: "Ruby",
    15: "Kotlin",
    16: "Rust",
    17: "Dart"    
}

# Memoria temporal (no persistente)
asignaciones_realizadas: dict[int, dict] = {}


# ------- Lógica -------
def distribuir_una_asignacion():
    """Asigna un lenguaje aleatorio a un alumno sin repetir (si quedan)."""
    if len(asignaciones_realizadas) >= len(alumnos):
        return None

    alumnos_disponibles = [k for k in alumnos if k not in asignaciones_realizadas]
    lenguajes_usados = {v["lenguaje_id"] for v in asignaciones_realizadas.values()}
    lenguajes_disponibles = [k for k in lenguajes_de_programacion if k not in lenguajes_usados]

    if not alumnos_disponibles or not lenguajes_disponibles:
        return None

    alumno_id = random.choice(alumnos_disponibles)
    lenguaje_id = random.choice(lenguajes_disponibles)

    asignaciones_realizadas[alumno_id] = {
        "nombre": alumnos[alumno_id],
        "lenguaje": lenguajes_de_programacion[lenguaje_id],
        "lenguaje_id": lenguaje_id
    }
    return {"id_alumno": alumno_id, "nombre": alumnos[alumno_id], "lenguaje": lenguajes_de_programacion[lenguaje_id]}


def estado_actual():
    """Devuelve estructura para UI."""
    listado = []
    for alumno_id, nombre in alumnos.items():
        if alumno_id in asignaciones_realizadas:
            lang = asignaciones_realizadas[alumno_id]["lenguaje"]
        else:
            lang = None
        listado.append({
            "id": alumno_id,
            "nombre": nombre,
            "lenguaje": lang
        })
    return {
        "total": len(alumnos),
        "asignados": len(asignaciones_realizadas),
        "completo": len(asignaciones_realizadas) >= len(alumnos),
        "items": listado
    }


# ------- Vistas -------
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request
    })


# ------- API para la página -------
@app.get("/api/status")
def api_status():
    return estado_actual()

@app.post("/api/distribuir")
def api_distribuir():
    distribuir_una_asignacion()
    # Devolver el nuevo estado para refrescar UI sin recargar
    return estado_actual()

@app.post("/api/reset")
def api_reset():
    asignaciones_realizadas.clear()
    return estado_actual()


# Salud
@app.get("/health")
def health():
    return {"status": "healthy"}
