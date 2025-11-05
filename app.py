from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
# ✅ Permite acceso desde cualquier origen (Flutter Web)
CORS(app, resources={r"/*": {"origins": "*"}})

LED_FILE = "leds.json"

# --- Inicialización ---
if not os.path.exists(LED_FILE):
    with open(LED_FILE, "w") as f:
        json.dump({"led1": False, "led2": False}, f)

# --- Leer estado ---
def leer_leds():
    with open(LED_FILE, "r") as f:
        return json.load(f)

# --- Guardar estado ---
def guardar_leds(data):
    with open(LED_FILE, "w") as f:
        json.dump(data, f)

# --- Rutas principales ---
@app.route("/led/status", methods=["GET"])
def led_status():
    leds = leer_leds()
    return jsonify(leds)

@app.route("/led/on/<led>", methods=["POST"])
def led_on(led):
    leds = leer_leds()
    if led in leds:
        leds[led] = True
        guardar_leds(leds)
        print(f"✅ {led} encendido")
        return jsonify({"message": f"{led} encendido"}), 200
    return jsonify({"error": "LED no encontrado"}), 404

@app.route("/led/off/<led>", methods=["POST"])
def led_off(led):
    leds = leer_leds()
    if led in leds:
        leds[led] = False
        guardar_leds(leds)
        print(f"🚫 {led} apagado")
        return jsonify({"message": f"{led} apagado"}), 200
    return jsonify({"error": "LED no encontrado"}), 404

# --- Página raíz ---
@app.route("/")
def home():
    return """
    <h2>✅ Servidor Flask ESP32 - Control de LEDs</h2>
    <p>Rutas disponibles:</p>
    <ul>
        <li>/led/status</li>
        <li>/led/on/1 o /led/on/2</li>
        <li>/led/off/1 o /led/off/2</li>
    </ul>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
