import sqlite3
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib

# Hämta temperaturer från SQLite-databas


def get_temperatures_from_db():
    conn = sqlite3.connect('data.db')  # Din databasfil
    c = conn.cursor()
    # Hämta alla temperaturer
    c.execute("SELECT temperature FROM temperature_log ORDER BY timestamp ASC")
    rows = c.fetchall()
    conn.close()
    return [row[0] for row in rows]  # Extrahera temperaturer till en lista


# Hämta temperaturdata från databasen
temps = get_temperatures_from_db()

X, y = [], []
window = 10  # Tidigare 10 temperaturer för att förutspå nästa
for i in range(len(temps) - window):
    X.append(temps[i:i+window])
    y.append(temps[i+window])

# Skapa och träna modellen som en linjär regression
model = LinearRegression()
model.fit(X, y)

# Spara modellen som en pickle-fil
joblib.dump(model, 'model.pkl')
