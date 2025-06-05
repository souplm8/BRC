# Local NTP Proxy Server

This Python script runs a local HTTP server that acts as a proxy to a real NTP server.  
It allows browser-based clocks (like BRC.html) to synchronize time using HTTP requests, even when they cannot access NTP directly.

## ✅ Features

- Converts NTP time to RESTful HTTP API
- Cross-platform (Windows, macOS, Linux)
- Accepts NTP server and port via query parameters
- CORS enabled for web clients

## 🔧 Requirements

- Python 3.6+
- `ntplib` library

## 🚀 Installation

### On macOS or Linux:

```bash
chmod +x install.sh
./install.sh
