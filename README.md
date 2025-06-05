# HTML BIG RED CLOCK with support fot timeapi.io and local NTP Proxy Server

🕒 BIG RED CLOCK – Local Time Server (time_server.py)

This Python-based HTTP server acts as a proxy between an NTP server and web clients.It provides a REST API endpoint for accessing synchronized time in JSON format.

📦 Installation

1. Unpack the ZIP:

unzip time_server_installers.zip
cd install

2. Run the installer for your operating system:

✅ Windows:

Double-click: install_windows.bat

Or run in terminal:

install_windows.bat

✅ macOS:

bash install_mac.sh

✅ Linux:

bash install_linux.sh

Each script will:

Create a Python virtual environment

Install ntplib (used for NTP time synchronization)

▶️ How to Start the Server

To run the server manually:

python3 /Users/oki/Documents/zegar/time_server.py

Or if using the virtual environment created during installation:

macOS/Linux:

cd /Users/oki/Documents/zegar
source venv/bin/activate
python time_server.py

Windows:

cd \Users\oki\Documents\zegar
venv\Scripts\activate.bat
python time_server.py

You will see:

NTP Time Proxy running on http://[your-IP]:15151/
Using NTP server: 192.168.7.20:123
Press Ctrl+C to stop the server.

⏹️ How to Stop the Server

To stop the server gracefully, press:

Ctrl + C

🌐 API Endpoint

The server exposes a time sync endpoint:

http://[your-server-ip]:15151/api/time?ntp=192.168.7.20:123

This URL can be configured in BRC.html under “Time source: Local time server”.

🧽 Time Source Switching

From your browser interface (BRC.html), you can:

Use a local NTP proxy server

Use a public API like https://timeapi.io

The server IP and port are configurable via input fields in the UI.
