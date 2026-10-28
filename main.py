from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Jarvis Cloud Controller")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Memoria global del sistema
estado_jarvis = {
    "tarea_actual": "Jarvis listo en PC Mark 3",
    "progreso": 100,
    "estado": "IDLE",
    "modulo": "Sistema",
    "comando_pendiente": None
}

class EstadoTarea(BaseModel):
    tarea_actual: str
    progreso: int
    estado: Optional[str] = "EN PROGRESO"
    modulo: Optional[str] = "General"
    comando_pendiente: Optional[str] = None

@app.get("/")
def home():
    return {"status": "Jarvis Cloud Server Online"}

@app.get("/obtener_estado")
def obtener_estado():
    return estado_jarvis

@app.post("/actualizar_estado")
def actualizar_estado(datos: EstadoTarea):
    global estado_jarvis
    payload = datos.dict(exclude_unset=True)
    estado_jarvis.update(payload)
    return {"status": "ok", "estado_actualizado": estado_jarvis}

@app.get("/obtener_comando")
def obtener_comando():
    global estado_jarvis
    cmd = estado_jarvis.get("comando_pendiente")
    # Una vez entregado el comando a la PC, se limpia de la cola
    if cmd:
        estado_jarvis["comando_pendiente"] = None
    return {"comando": cmd}