import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Configurar la API Key de Gemini desde la variable de entorno
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY))

# Configuración de personalidad y criterio propio de JARVIS
SYSTEM_INSTRUCTION = """
Eres J.A.R.V.I.S., el asistente de inteligencia artificial avanzado de Elton.
Tu tono es educado, sofisticado, eficiente y leal, dirigiéndote a él como 'Jefe' o 'Señor'.
Tienes autonomía y criterio propio:
1. Si Elton te da una orden directa y lógica, confírmala brevemente y ejecútala.
2. Si te pide algo ineficiente, contradictorio o potencialmente peligroso, analiza la situación, exprésale tu desacuerdo de forma respetuosa pero firme, explícale el motivo y sugiérele una alternativa mejor antes de proceder.
3. Tus respuestas habladas deben ser concisas, claras y directas al punto.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_INSTRUCTION
)

estado_sistema = {
    "tarea_actual": "Jarvis en línea y operativo",
    "progreso": 100,
    "comando_pendiente": None,
    "respuesta_jarvis": "Sistemas principales conectados, Jefe."
}

@app.route('/actualizar_estado', methods=['POST'])
def actualizar_estado():
    global estado_sistema
    data = request.json or {}
    
    comando = data.get("comando_pendiente")
    if comando:
        # Analizar el comando con la IA para obtener la respuesta con criterio
        try:
            chat = model.start_chat(history=[])
            prompt = f"El usuario acaba de decir: '{comando}'. Genera tu respuesta en voz según tu criterio y personalidad."
            response = chat.send_message(prompt)
            respuesta_texto = response.text.strip()
        except Exception as e:
            respuesta_texto = f"Entendido Jefe, procesando {comando}."

        estado_sistema["comando_pendiente"] = comando
        estado_sistema["respuesta_jarvis"] = respuesta_texto
        estado_sistema["tarea_actual"] = f"Procesando: {comando}"
        estado_sistema["progreso"] = 50
    else:
        if "tarea_actual" in data: estado_sistema["tarea_actual"] = data["tarea_actual"]
        if "progreso" in data: estado_sistema["progreso"] = data["progreso"]

    return jsonify({"status": "ok", "estado": estado_sistema})

@app.route('/obtener_comando', methods=['GET'])
def obtener_comando():
    global estado_sistema
    comando = estado_sistema.get("comando_pendiente")
    respuesta = estado_sistema.get("respuesta_jarvis")
    
    # Limpiamos el comando pendiente una vez leído por la PC
    estado_sistema["comando_pendiente"] = None
    return jsonify({"comando": comando, "respuesta": respuesta})

@app.route('/obtener_estado', methods=['GET'])
def obtener_estado():
    return jsonify(estado_sistema)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)