#include <ESP8266WiFi.h>
#include <FirebaseArduino.h>
#include "DHT.h"
#define DHTType DHT11
float humidity;
float temperatureC;
float temperatureF;

#define FIREBASE_HOST "smarthome-6ad5a-default-rtdb.firebaseio.com"
#define FIREBASE_AUTH "FPpQ10lDZV6OzQXLoVycJRRV2VUT8i28bmMrdxtQ"
#define WIFI_SSID "banh"
#define WIFI_PASSWORD "12345678"

int led_pin = 5; //D1
int led_val = 0;
int dht_pin = 4; //D2

DHT HT(dht_pin,DHTType);

void setup() {
  pinMode(led_pin,OUTPUT);
  HT.begin();

  Serial.begin(9600);

  // connect to wifi.
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("connecting");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("connected: ");
  Serial.println(WiFi.localIP());
  
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
}

void loop() {
  led_val = Firebase.getInt("light");
  if (led_val == 1){
    digitalWrite(led_pin, HIGH);
  } else {
    digitalWrite(led_pin, LOW);
  }

  
  humidity = HT.readHumidity();
  temperatureC = HT.readTemperature();
  temperatureF = HT.readTemperature(true);
  Firebase.setFloat("hum", humidity);
  Firebase.setFloat("tempC", temperatureC);
  Firebase.setFloat("tempF", temperatureF);



  // delay(500);
}
