# importar fastapi
from fastapi import FastAPI
import random

app = FastAPI()

alumnos = {
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

lenguajes_de_programacion = {
    1: "JavaScript",
    2: "PHP",
    3: "Java",
    4: "Python",
    5: "Ruby",
    6: "Kotlin",
    7: "Rust",
    8: "Dart",
    9: "C#"
}

# 🧠 Memoria temporal de asignaciones (no persistente)
asignaciones_realizadas = {}

# ---- Funciones auxiliares ----
def obtener_alumno_aleatorio():
    clave = random.choice(list(alumnos.keys()))
    return alumnos[clave]

def obtener_asignacion():
    """Devuelve una pareja alumno + lenguaje no repetida."""
    # Ver si ya se repartieron todos
    if len(asignaciones_realizadas) >= len(alumnos):
        return {"mensaje": "✅ Todos los alumnos ya tienen un lenguaje asignado."}
    
    # Escoger alumno que aún no tenga lenguaje
    alumnos_disponibles = [k for k in alumnos if k not in asignaciones_realizadas]
    alumno_id = random.choice(alumnos_disponibles)
    
    # Escoger lenguaje que aún no haya sido usado
    lenguajes_disponibles = [
        k for k in lenguajes_de_programacion
        if k not in [v["lenguaje_id"] for v in asignaciones_realizadas.values()]
    ]
    lenguaje_id = random.choice(lenguajes_disponibles)
    
    # Registrar asignación
    asignaciones_realizadas[alumno_id] = {
        "nombre": alumnos[alumno_id],
        "lenguaje": lenguajes_de_programacion[lenguaje_id],
        "lenguaje_id": lenguaje_id
    }
    
    return {
        "id_alumno": alumno_id,
        "nombre": alumnos[alumno_id],
        "lenguaje": lenguajes_de_programacion[lenguaje_id]
    }

# ---- Endpoints ----
@app.get("/health")
def read_root():
    return {"status": "healthy"}

@app.get("/alumno")
def alumno_aleatorio():
    clave = random.choice(list(alumnos.keys()))
    return {"id": clave, "nombre": alumnos[clave]}

@app.get("/distribuir")
def distribuir_alumno_lenguaje():
    """Distribuye un alumno con un lenguaje aleatorio (sin repetir)."""
    return obtener_asignacion()

@app.get("/asignaciones")
def ver_asignaciones():
    """Devuelve todas las asignaciones actuales."""
    return asignaciones_realizadas
