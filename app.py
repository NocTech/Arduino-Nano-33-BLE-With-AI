from flask import Flask, render_template, request, jsonify
import sqlite3
import joblib
import numpy as np
from datetime import datetime
import serial  # pyserial för Arduino-kommunikation
import threading

app = Flask(__name__)

# Försök ladda ML-modellen
try:
    model = joblib.load('model.pkl')
except Exception as e:
    print(f"Misslyckades med att ladda modellen: {e}")
    model = None

# Konfiguration för Arduino
ARDUINO_PORT = 'COM7'  # Ändra vid behov
BAUD_RATE = 9600


# Initiera SQLite-databasen
def init_db():
    with sqlite3.connect("data.db") as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS temperature_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                temperature REAL NOT NULL
            )
        ''')
        conn.commit()


# Hämta senaste N temperaturer
def get_latest_temperatures(n=10):
    with sqlite3.connect("data.db") as conn:
        c = conn.cursor()
        c.execute("SELECT temperature FROM temperature_log ORDER BY timestamp DESC LIMIT ?", (n,))
        rows = c.fetchall()
    return [row[0] for row in reversed(rows)]


# Logga temperatur i databasen
def log_temperature(temp):
    now = datetime.utcnow().isoformat()
    with sqlite3.connect("data.db") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO temperature_log (timestamp, temperature) VALUES (?, ?)", (now, temp))
        conn.commit()


# Läs data från Arduino
def read_from_arduino():
    try:
        arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
        while True:
            line = arduino.readline().decode('utf-8').strip()
            if line:
                try:
                    temperature = float(line)
                    log_temperature(temperature)
                    print(f"Logged temperature: {temperature}")
                except ValueError:
                    print(f"Invalid data received: {line}")
    except serial.SerialException as e:
        print(f"Error connecting to Arduino: {e}")


# Startsida
@app.route("/")
def index():
    return render_template("index.html")


# Kombinerad GET och POST för temperatur
@app.route("/api/temperature", methods=["GET", "POST"])
def temperature_api():
    if request.method == "POST":
        data = request.get_json()
        try:
            temperature = float(data.get("temperature"))
            log_temperature(temperature)
            return jsonify({"status": "success", "temperature": temperature}), 200
        except (TypeError, ValueError):
            return jsonify({"status": "error", "message": "Invalid temperature format"}), 400

    elif request.method == "GET":
        with sqlite3.connect("data.db") as conn:
            c = conn.cursor()
            c.execute("SELECT timestamp, temperature FROM temperature_log ORDER BY timestamp DESC LIMIT 1")
            row = c.fetchone()
        if row:
            return jsonify({"status": "success", "temperature": row[1], "timestamp": row[0]}), 200
        else:
            return jsonify({"status": "error", "message": "No data available"}), 404


# Prediktion av nästa temperatur
@app.route("/api/predict", methods=["GET"])
def predict_temperature():
    if model is None:
        return jsonify({"status": "error", "message": "Model not available."}), 500

    latest_temperatures = get_latest_temperatures(10)
    if len(latest_temperatures) < 10:
        return jsonify({"status": "error", "message": "Not enough data to make a prediction."}), 400

    X_input = np.array(latest_temperatures).reshape(1, -1)
    predicted_temp = model.predict(X_input)[0]
    return jsonify({"status": "success", "predicted_temperature": predicted_temp}), 200


# Hämta de senaste temperaturerna (logg)
@app.route("/api/temperature_log", methods=["GET"])
def get_temperature_log():
    with sqlite3.connect("data.db") as conn:
        c = conn.cursor()
        c.execute("SELECT timestamp, temperature FROM temperature_log ORDER BY timestamp DESC LIMIT 10")
        rows = c.fetchall()

    temperatures = [{"timestamp": row[0], "temperature": row[1]} for row in rows]
    return jsonify({"status": "success", "temperatures": temperatures})


# Kör servern
if __name__ == "__main__":
    init_db()
    arduino_thread = threading.Thread(target=read_from_arduino, daemon=True)
    arduino_thread.start()
    app.run(debug=True, host='0.0.0.0', port=5000)
