# Temperaturövervakning med Prediktion (Linjär regressionsmodell)

Detta projekt övervakar temperatur med en Arduino och visualiserar samt förutspår temperaturdata med hjälp av en webbapplikation och maskininlärning.

## Funktioner

- Läser temperatur från en DHT11-sensor kopplad till en Arduino Nano 33 BLE.
- Loggar temperaturdata till en SQLite-databas.
- Tränar en linjär regressionsmodell för att förutspå framtida temperaturer.
- Visar senaste temperatur, prediktion och trend i ett webbgränssnitt (Flask + Chart.js).
- Automatisk uppdatering av data i realtid.

## Filstruktur

- `app.py` – Flask-server, API och webbgränssnitt.
- `db.py` – Initiering och loggning av temperatur till SQLite.
- `train_model.py` – Tränar ML-modell på data från databasen.
- `train_model_csv.py` – Tränar ML-modell på data från CSV-fil.
- `model.pkl` – Sparad ML-modell.
- `data.db` – SQLite-databas med temperaturdata.
- `Arduino/sketch_may12a.ino` – Arduino-kod för att läsa temperatur och skicka via serieport.
- `static/script.js` – Frontend-JavaScript för att hämta och visa data.
- `templates/index.html` – Webbgränssnittets HTML.

## Installation

1. **Krav**  
   - Python 
   - pip  
   - Arduino IDE  
   - DHT11-sensor  
   - Arduino Nano 33 BLE  
   - PySerial, Flask, scikit-learn, joblib, pandas, numpy

2. **Installera Python-paket**  
   ```sh
   pip install flask pyserial scikit-learn joblib pandas numpy
   ```

3. **Ladda upp Arduino-koden**  
   - Öppna `Arduino/sketch_may12a.ino` i Arduino IDE.
   - Ladda upp till din Arduino Nano 33 BLE.

4. **Starta webbservern**  
   ```sh
   python app.py
   ```

5. **Träna ML-modellen**  
   - Efter att ha samlat in data, kör:
     ```sh
     python train_model.py
     ```
   - Alternativt, om du har en CSV-fil:
     ```sh
     python train_model_csv.py
     ```

6. **Öppna webbläsaren**  
   - Gå till [http://localhost:5000](http://localhost:5000)

## API-endpoints

- `GET /api/temperature` – Hämtar senaste temperatur.
- `POST /api/temperature` – Loggar ny temperatur (JSON: `{ "temperature": <float> }`).
- `GET /api/predict` – Hämtar predikterad temperatur om 10 minuter.
- `GET /api/temperature_log` – Hämtar de senaste 10 temperaturmätningarna.

