from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Estado inicial de los LEDs
leds = {"led1": False, "led2": False}

@app.route('/')
def home():
    return "<h2>Servidor ESP32 Control de LEDs</h2><p>Usa /led/on o /led/off con parámetros para controlar.</p>"

@app.route('/led/on', methods=['GET'])
def led_on():
    led = request.args.get('led')
    if led in leds:
        leds[led] = True
        print(f"{led} encendido")
        return jsonify({"status": "ok", "led": led, "state": "on"})
    return jsonify({"error": "LED no encontrado"}), 404

@app.route('/led/off', methods=['GET'])
def led_off():
    led = request.args.get('led')
    if led in leds:
        leds[led] = False
        print(f"{led} apagado")
        return jsonify({"status": "ok", "led": led, "state": "off"})
    return jsonify({"error": "LED no encontrado"}), 404

@app.route('/led/status', methods=['GET'])
def led_status():
    return jsonify(leds)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
