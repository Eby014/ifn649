#include "DHT.h"

#define DHTPIN 21      // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11   // DHT 11

#define LEDPIN 11

DHT dht(DHTPIN, DHTTYPE);


void setup() {
  // Setup serial for monitor
  Serial.begin(9600); 
  Serial.write("SERIAL: Beginning communication....");

  // Setup DHT Sensor
  pinMode(DHTPIN, INPUT);
  dht.begin();

  // Setup Serial1 for BlueTooth
  Serial1.begin(9600); // Default communication rate of the Bluetooth module
  Serial1.write("SERIAL1: Beginning communication....");
}

void loop() {
  //(Serial1.available() > 0){ // Checks whether data is comming from the serial port
    if (Serial1.available() > 0){
      // while(Serial1.read()){
        Serial.printf("%s",Serial1.readString());
      // }
    }
    if (Serial.available() > 0){
      // while(Serial.read()){
        Serial1.write(Serial.read());
      // }
    }
    digitalWrite(LEDPIN, HIGH);
    
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    float f = dht.readTemperature(true);

    char hif[6], hic[6], f_s[6],t_s[6],h_s[6];
    dtostrf(f,4,2,f_s);
    dtostrf(h,4,2,h_s);
    dtostrf(t,4,2,t_s);
    dtostrf(dht.computeHeatIndex(f, h),4,2,hif);
    dtostrf(dht.computeHeatIndex(t, h, false),4,2,hic);

    char final_buffer[256];

    sprintf(final_buffer, " Humidity: %s | Temperature: %sC /%sF | Heat index: %sC /%sF\n", h_s, t_s, f_s,hic, hif);
    Serial.write(final_buffer);
    Serial1.write(final_buffer);

    delay(1000);
    
    digitalWrite(LEDPIN, LOW);
    delay(1000);
}