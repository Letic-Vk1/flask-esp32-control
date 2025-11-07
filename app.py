from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

LED_FILE = "leds.json"

if not os.path.exists(LED_FILE):
    with open(LED_FILE, "w") as f:
        json.dump({"led1": False, "led2": False}, f)

def leer_leds():
    with open(LED_FILE, "r") as f:
        return json.load(f)

def guardar_leds(data):
    with open(LED_FILE, "w") as f:
        json.dump(data, f)

@app.route("/led/status", methods=["GET"])
def led_status():
    leds = leer_leds()
    return jsonify(leds)

@app.route("/led/on/<led>", methods=["POST"])
def led_on(led):
    leds = leer_leds()
    led_key = f"led{led}" if led.isdigit() else led
    if led_key in leds:
        leds[led_key] = True
        guardar_leds(leds)
        print(f"✅ {led_key} encendido")
        return jsonify({"message": f"{led_key} encendido"}), 200
    return jsonify({"error": "LED no encontrado"}), 404

@app.route("/led/off/<led>", methods=["POST"])
def led_off(led):
    leds = leer_leds()
    led_key = f"led{led}" if led.isdigit() else led
    if led_key in leds:
        leds[led_key] = False
        guardar_leds(leds)
        print(f"🚫 {led_key} apagado")
        return jsonify({"message": f"{led_key} apagado"}), 200
    return jsonify({"error": "LED no encontrado"}), 404

@app.route("/")
def home():
    return """
    <h2>✅ Servidor Flask ESP32 - Control de LEDs</h2>
    <ul>
        <li>/led/status</li>
        <li>/led/on/1 o /led/on/led1</li>
        <li>/led/off/1 o /led/off/led1</li>
    </ul>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
