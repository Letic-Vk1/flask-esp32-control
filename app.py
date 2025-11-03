from flask import Flask, request, jsonify

app = Flask(__name__)

# Estado inicial de los LEDs
leds = {"led1": False, "led2": False}

@app.route('/')
def home():
    return "<h2>Servidor ESP32 Control de LEDs</h2><p>Usa /led/on o /led/off con parámetros para controlar.</p>"

# Endpoint para encender un LED
@app.route('/led/on', methods=['GET'])
def led_on():
    led = request.args.get('led')
    if led in leds:
        leds[led] = True
        print(f"{led} encendido")
        return jsonify({"status": "ok", "led": led, "state": "on"})
    return jsonify({"error": "LED no encontrado"}), 404

# Endpoint para apagar un LED
@app.route('/led/off', methods=['GET'])
def led_off():
    led = request.args.get('led')
    if led in leds:
        leds[led] = False
        print(f"{led} apagado")
        return jsonify({"status": "ok", "led": led, "state": "off"})
    return jsonify({"error": "LED no encontrado"}), 404

# Endpoint para consultar el estado
@app.route('/led/status', methods=['GET'])
def led_status():
    return jsonify(leds)

# 🔹 Esta parte es la que ejecuta el servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
