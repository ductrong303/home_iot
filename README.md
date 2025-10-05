# STM32F401 + BMP280 + ESP8266 IoT Home

This project uses an **STM32F401** microcontroller to read temperature and pressure data from a **BMP280** sensor via **I2C**, display the readings on an **LCD**, and transmit them over **UART** to an **ESP8266 (NodeMCU ESP-12E)** module.  
The ESP8266 runs a **custom Arduino-based firmware** (since the original AT firmware was removed and not fully compatible) to forward the readings over Wi-Fi to a **Python web server** for live monitoring.

---

## System Overview


---

## Features

- Reads temperature and air pressure from BMP280 using I2C  
- Displays values on a 16x2 LCD connected to the STM32  
- Sends readings to an ESP8266 module via UART  
- ESP8266 runs Arduino firmware to post data to a web server  
- Python script hosts a web page showing the latest readings, refreshed automatically  
- Modular design: STM32 handles sensors and display, ESP8266 handles Wi-Fi communication

---

## Hardware Components

| Component | Description |
|------------|-------------|
| STM32F401RE (Nucleo or similar) | Main controller |
| BMP280 Sensor | I2C temperature and pressure sensor |
| 16x2 LCD Display | Local visual output |
| ESP8266 NodeMCU (ESP-12E) | Wi-Fi module for transmitting data |
| PC or Laptop | Runs Python web server |

---

## Software & Tools

| Tool | Purpose |
|------|----------|
| STM32CubeIDE | STM32 firmware development |
| Arduino IDE | Programming ESP8266 firmware |
| Python 3 | Running the local web server |
| BMP280 Library | Sensor communication |
| Wi-Fi Client (ESP8266) | HTTP POST communication to server |

---

## How It Works

1. The STM32F401 reads temperature and pressure data from the BMP280 sensor using I2C.  
2. The data is displayed on the LCD for local viewing.  
3. The STM32 then sends the readings via UART to the ESP8266.  
4. The ESP8266, programmed using the Arduino IDE, connects to the Wi-Fi network and posts the data to the Python web server running on the PC.  
5. The Python server displays the readings on a live-updating webpage that refreshes every second.

---

## ESP8266 Firmware Notes

The ESP8266’s original AT firmware was removed because it caused compatibility issues.  
It now runs a custom Arduino sketch, which handles:
- Wi-Fi connection (SSID and password configured in code)
- Sending sensor data via HTTP POST to the web server

---

## Python Web Server

A simple Python script (`live_server.py`) is included.  
It uses the `http.server` library to:
- Accept POST requests from the ESP8266 containing sensor readings  
- Serve a web page showing the latest temperature and pressure, auto-refreshed every second

Run the server using:
```bash
python live_server.py
