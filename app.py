from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

LED_FILE = "leds.json"

# Cargar estado inicial de los LEDs desde archivo JSON
def cargar_estado():
    if os.path.exists(LED_FILE):
        with open(LED_FILE, "r") as f:
            return json.load(f)
    return {"led1": False, "led2": False}

# Guardar estado actual de los LEDs
def guardar_estado(estado):
    with open(LED_FILE, "w") as f:
        json.dump(estado, f)

leds = cargar_estado()

@app.route("/")
def home():
    return "<h2>Servidor ESP32 Control de LEDs</h2><p>Endpoints: /led/on, /led/off, /led/status</p>"

@app.route("/led/on", methods=["GET"])
def led_on():
    led = request.args.get("led")
    if led in leds:
        leds[led] = True
        guardar_estado(leds)
        print(f"{led} encendido")
        return jsonify({"status": "ok", "led": led, "state": "on"})
    return jsonify({"error": "LED no encontrado"}), 404

@app.route("/led/off", methods=["GET"])
def led_off():
    led = request.args.get("led")
    if led in leds:
        leds[led] = False
        guardar_estado(leds)
        print(f"{led} apagado")
        return jsonify({"status": "ok", "led": led, "state": "off"})
    return jsonify({"error": "LED no encontrado"}), 404

@app.route("/led/status", methods=["GET"])
def led_status():
    return jsonify(leds)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
