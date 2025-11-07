from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
# ✅ Permite acceso desde cualquier origen (para app Flutter y ESP32)
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

@app.route("/led/on/<led>", methods=["GET", "POST"])
def led_on(led):
    leds = leer_leds()
    if led in leds:
        leds[led] = True
        guardar_leds(leds)
        print(f"✅ {led} encendido")
        return jsonify({"message": f"{led} encendido"}), 200
    return jsonify({"error": "LED no encontrado"}), 404

@app.route("/led/off/<led>", methods=["GET", "POST"])
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
        <li><a href="/led/status">/led/status</a></li>
        <li><a href="/led/on/led1">/led/on/led1</a></li>
        <li><a href="/led/off/led1">/led/off/led1</a></li>
        <li><a href="/led/on/led2">/led/on/led2</a></li>
        <li><a href="/led/off/led2">/led/off/led2</a></li>
    </ul>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
