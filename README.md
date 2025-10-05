# STM32F401 + BMP280 + ESP8266 IoT Home

This project uses an **STM32F401** to measure temperature and pressure with a **BMP280** sensor via **I2C**, display the data on an **LCD**, and send it to an **ESP8266 (NodeMCU ESP-12E)** using **UART**.  
The ESP8266, programmed with a custom **Arduino firmware**, transmits readings over Wi-Fi to a **Python web server** for live monitoring in a browser.

---

## System Overview

[BMP280] --I2C--> [STM32F401] --UART--> [ESP8266] --Wi-Fi--> [Python Web Server]

---

## Features

- Reads temperature and pressure using BMP280  
- Displays values on a 16x2 LCD  
- LCD brightness adjustable via potentiometer  
- Sends data to ESP8266 via UART  
- ESP8266 posts readings to a Python web server  
- Web page auto-refreshes every second

---

## Hardware

| Component | Function |
|------------|-----------|
| STM32F401RE | Main microcontroller |
| BMP280 | I2C temperature & pressure sensor |
| 16x2 LCD | Displays readings locally |
| Potentiometer | Adjusts LCD brightness |
| ESP8266 NodeMCU | Wi-Fi transmission |
| PC | Runs Python web server |

---

## Software

- **STM32CubeIDE** – STM32 firmware  
- **Arduino IDE** – ESP8266 firmware  
- **Python 3** – `live_server.py` web server
- 
## Images

System Setup:
![553454542_3254298758062209_3833673561105896772_n](https://github.com/user-attachments/assets/4dcbbc2a-f2ea-4a1a-9397-7a200dc57e9b)

Browser Screenshot:
![553303486_652400094331798_1516934589024052846_n](https://github.com/user-attachments/assets/8be200f1-988b-4c1c-9c84-7c03fd4ae0fb)

