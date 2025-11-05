from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

# --- Configuración del servidor Flask ---
app = Flask(__name__)
CORS(app)  # Permitir peticiones desde Flutter Web

# --- Archivo donde se guardan los estados ---
LED_FILE = "leds.json"

# --- Función para leer el estado de los LEDs ---
def leer_estado_leds():
    if not os.path.exists(LED_FILE):
        # Si no existe el archivo, se crea con los LEDs apagados
        estado_inicial = {"led1": False, "led2": False}
        with open(LED_FILE, "w") as f:
            json.dump(estado_inicial, f)
        return estado_inicial

    with open(LED_FILE, "r") as f:
        return json.load(f)

# --- Función para guardar el estado de los LEDs ---
def guardar_estado_leds(estado):
    with open(LED_FILE, "w") as f:
        json.dump(estado, f)

# --- Ruta raíz ---
@app.route('/')
def home():
    return "<h2>Servidor Flask activo ✅</h2><p>Usa /led/status para ver el estado de los LEDs.</p>"

# --- Ruta para obtener el estado de los LEDs ---
@app.route('/led/status', methods=['GET'])
def obtener_estado_leds():
    estado = leer_estado_leds()
    return jsonify(estado)

# --- Ruta para cambiar el estado de un LED ---
@app.route('/led/<led_id>', methods=['POST'])
def cambiar_estado_led(led_id):
    estado = leer_estado_leds()
    data = request.get_json()

    if led_id not in estado:
        return jsonify({"error": "LED no encontrado"}), 404

    if "state" not in data:
        return jsonify({"error": "Falta el parámetro 'state'"}), 400

    # Actualizar el estado
    nuevo_estado = bool(data["state"])
    estado[led_id] = nuevo_estado
    guardar_estado_leds(estado)

    return jsonify({
        "message": f"Estado de {led_id} actualizado",
        "new_state": nuevo_estado
    })

# --- Ejecución local ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
