#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "env.h"

const char* putendpoint = API_URL_PUT;
const char* getendpoint = API_URL_GET;

const int fanpin = 22;
const int lightpin = 23;

float float_rand(float min,float max)
{
    float scale = rand() / (float) RAND_MAX; /* [0, 1.0] */
    return min + scale * (max-min);      /* [min, max] */
}
void getmethod();
void putmethod();

void setup() {
  Serial.begin(9600);
  pinMode(fanpin, OUTPUT);
  pinMode(lightpin, OUTPUT);

  WiFi.begin(WIFI_USER, WIFI_PASS);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("The Bluetooth Device is Ready to Pair");
  Serial.println("Connected @");
  Serial.print(WiFi.localIP());
}

void loop() {
  //Check WiFi connection status
  if(WiFi.status()== WL_CONNECTED){
   
   putmethod();
   getmethod();
    
  }
  else {
    Serial.println("WiFi Disconnected");
  }
}

void getmethod(){
  
    HTTPClient http;


    String url = getendpoint;    
    http.begin(url);
    int httpResponseCode = http.GET();
    String http_response;

    Serial.println("");
    Serial.println("");

    if (httpResponseCode>0) {
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);

        Serial.print("Response:");
        http_response = http.getString();
        Serial.println(http_response);
      }
      else {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
    }
  
    StaticJsonDocument<1024> docget;

    DeserializationError error = deserializeJson(docget, http_response);

    if (error) {
      Serial.print("deserializeJson() failed: ");
      Serial.println(error.c_str());
      return;
    }
    
    bool temp = docget["fan"]; 
    bool light= docget["light"]; 

    digitalWrite(fanpin,temp);
    digitalWrite(lightpin,light);
    
    // Free resources
    http.end();
}

void putmethod(){
    
    Serial.println("");
    HTTPClient http;
  
    // Establish a connection to the server
    String url = putendpoint;
    http.begin(url);
    http.addHeader("Content-type", "application/json");

    StaticJsonDocument<1024> docput;
    String httpRequestData;

    docput["temperature"] = float_rand(21.0,33.0);

    serializeJson(docput, httpRequestData);

    // Send HTTP PUT request
    int httpResponseCode = http.PUT(httpRequestData);
    String http_response;

    // check reuslt of PUT request. negative response code means server wasn't reached
    if (httpResponseCode>0) {
      Serial.println("PUT Attempted");
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
    }
    else {
      Serial.print("Error code:");
      Serial.println(httpResponseCode);
    }

    http.end();
}