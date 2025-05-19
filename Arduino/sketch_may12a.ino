#include <DHT.h>
#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  float temp = dht.readTemperature();
  
  if (!isnan(temp)) {
    Serial.println(temp);
  }
  delay(30000); // Mäta varje minut
}