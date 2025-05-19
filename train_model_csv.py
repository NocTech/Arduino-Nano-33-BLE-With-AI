import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib

# Läs temperaturdata från CSV
data = pd.read_csv('temperatures.csv', parse_dates=['timestamp'])

# Extrahera temperaturvärden
temps = data['temperature'].values

X, y = [], []
window = 10  # Tidigare 10 temperaturer för att förutspå nästa
for i in range(len(temps) - window):
    X.append(temps[i:i+window])
    y.append(temps[i+window])

# Skapa och träna modellen
model = LinearRegression()
model.fit(X, y)

# Spara modellen som en pickle-fil
joblib.dump(model, 'model.pkl')
