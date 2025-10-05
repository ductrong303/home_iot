#include <ESP8266WiFi.h>

// NETWORK CONFIGURATION
const char* ssid     = "xxx";
const char* password = "xxx";
const char* host = "x.x.x.x";   // IP address of PC running the web server
const uint16_t port = 8080;          // port server listens on

// UART CONFIG
const long STM_BAUD = 115200; //STM32 UART baud.
String lineBuf; // Line buffering
const size_t MAX_LINE = 512;    // safety cap
const uint32_t SEND_COOLDOWN_MS = 5; // small pause after send

// HTTP Post routine
void sendToServer(const String& payload) {
  // Create wifi client connect to host:port
  WiFiClient client;
  if (!client.connect(host, port)) {
    return;
  }

  // HTTP POST with raw JSON payload
  // HTTP header 
  client.println("POST / HTTP/1.1"); //making a POST request to path / using HTTP version 1.1
  client.print("Host: "); client.println(host); // Host header, tells which hostname is the script talking to
  client.println("Content-Type: application/json"); // Data type is being sent
  client.print("Content-Length: "); client.println(payload.length()); // Tells server how many bytes of body data will follow
  client.println("Connection: close");
  client.println(); //separates HTTP headers from message body
  //Actual message
  client.print(payload);

  //Optionally read response
  uint32_t t0 = millis();
  while (millis() - t0 < 1000) {  //Loop for max 1s
    while (client.available()) client.read(); //Read and discard replies from server
    if (!client.connected()) break; //Exit if connection closed
    delay(1);
  }
  client.stop();
}


void setup() {
  //Start UART0 for STM32 input/output on ESP8266 RX
  Serial.begin(STM_BAUD); // Init Serial object for UART0 of ESP
  delay(50);

  //WiFi object of ESP8266
  WiFi.mode(WIFI_STA); //STA=Station - ESP joins existing networks
  WiFi.begin(ssid, password);
  uint32_t t0 = millis();
  while (WiFi.status() != WL_CONNECTED && (millis() - t0) < 20000) {
    delay(200); //Wait for Wifi connection
  }
}

void loop() {
  //Non-blocking read from hardware UART
  while (Serial.available()) { //Only read when UART has something
    char c = (char)Serial.read();

    if (lineBuf.length() < MAX_LINE) {
      lineBuf += c;
    } else {
      //If line grows too large, drop until newline to resync
    }
    if (c == '\n') { //Full line received. Forward it exactly as received.
      
      String msg = lineBuf;   // includes '\n'
      lineBuf = ""; //Clear linebug
      sendToServer(msg); //Sending string to server
      delay(SEND_COOLDOWN_MS);
    }
  }
  // Yield to WiFi stack
  delay(1);
}