#include <ESP8266WiFi.h>
#include <FirebaseArduino.h>
#include "DHT.h"
#include <Servo.h>

#define DHTType DHT11


#define FIREBASE_HOST "smarthome-6ad5a-default-rtdb.firebaseio.com"
#define FIREBASE_AUTH "FPpQ10lDZV6OzQXLoVycJRRV2VUT8i28bmMrdxtQ"

// #define WIFI_SSID "banh"
// #define WIFI_PASSWORD "12345678"
#define WIFI_SSID "mangmiennui"
#define WIFI_PASSWORD "bkdn2003"

int led_pin = 5; // D1
int led_val;

int dht_pin = 4; // D2
float humidity;
float temperatureC;
float temperatureF;

int rheostat_pin = 0; // A0
int rheostat_val;

int servo_pin = 0; // D3
int servo_val;

int door;
int open_door = 0;
DHT HT(dht_pin,DHTType);
Servo servo;

void setup() {
  pinMode(led_pin,OUTPUT);
  HT.begin();
  servo.attach(servo_pin);

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


  door = Firebase.getInt("door");
  rheostat_val = analogRead(rheostat_pin);
  Firebase.setInt("rheostat",rheostat_val);

  if (door && open_door && rheostat_val<10) {
    door = 0;
    open_door = 0;
    Firebase.setInt("door",0);
  }

  if (door) {
    servo_val = 0;
  } else {
    servo_val = 90;
  }
  servo.write(servo_val);
  Firebase.setInt("servo",servo_val);


  if (door &&  rheostat_val>=10){
    open_door = 1;
  } else {
    open_door = 0;
  }

  Serial.print(door); Serial.print(" "); 
  Serial.print(open_door); Serial.print(" "); 
  Serial.print(rheostat_val); Serial.print(" ");
  Serial.println(servo_val);





}
