# time_server.py
# A simple HTTP server that acts as a proxy for NTP time, exposing a REST API endpoint.
# The server fetches time from a configured NTP server and provides it as JSON via HTTP,
# allowing web clients to synchronize their clocks with local or remote NTP sources.

import socket
import threading
import signal
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import ntplib
from datetime import datetime, timezone

# --- NTP address for time fetching (change as needed)
DEFAULT_NTP_SERVER = "192.168.7.20"
DEFAULT_NTP_PORT = 123

#
# HTTP request handler for the time API.
# Responds to GET requests at /api/time, fetching time from the specified NTP server.
#
class TimeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Handle GET requests for the /api/time endpoint
        from urllib.parse import urlparse, parse_qs
        parsed_url = urlparse(self.path)
        if parsed_url.path == "/api/time":
            try:
                # Parse query parameters to determine NTP server and port
                query_params = parse_qs(parsed_url.query)
                ntp_param = query_params.get("ntp", [f"{DEFAULT_NTP_SERVER}:{DEFAULT_NTP_PORT}"])[0]
                if ":" in ntp_param:
                    ntp_host, ntp_port = ntp_param.split(":", 1)
                    ntp_host = ntp_host.strip()
                    try:
                        ntp_port = int(ntp_port)
                    except Exception:
                        raise ValueError("Invalid NTP port")
                else:
                    ntp_host = ntp_param.strip()
                    ntp_port = DEFAULT_NTP_PORT
                # Query the NTP server for current time
                client = ntplib.NTPClient()
                response = client.request(ntp_host, port=ntp_port, version=3)
                dt = datetime.fromtimestamp(response.tx_time, timezone.utc)
                response_json = {'utc': dt.isoformat()}
                # Send successful JSON response with UTC time
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(response_json).encode())
            except Exception as e:
                # Send error response if NTP fetch fails
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                error_json = {"error": f"NTP error: {str(e)}"}
                self.wfile.write(json.dumps(error_json).encode())
        else:
            # Respond with 404 for any other endpoint
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            error_json = {"error": "Not found"}
            self.wfile.write(json.dumps(error_json).encode())


#
# Get the local IP address of the machine (used for displaying the server URL).
#
def get_local_ip():
    # Returns the local IP address used for outbound connections (not 127.0.0.1)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Use a public IP to determine the outbound interface, doesn't send packets
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

#
# Start the HTTP server in a separate thread and handle graceful shutdown on Ctrl+C.
#
def run_server():
    server_address = ("0.0.0.0", 15151)
    httpd = HTTPServer(server_address, TimeHandler)
    ip = get_local_ip()

    print(f"NTP Time Proxy running on http://{ip}:15151/")
    print(f"Using NTP server: {DEFAULT_NTP_SERVER}:{DEFAULT_NTP_PORT}")
    print("Press Ctrl+C to stop the server.")

    def serve():
        try:
            httpd.serve_forever()
        except Exception as e:
            print(f"Server error: {e}")

    server_thread = threading.Thread(target=serve, daemon=True)
    server_thread.start()

    def shutdown_server(signum, frame):
        print("\nShutting down server...")
        httpd.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown_server)
    signal.signal(signal.SIGTERM, shutdown_server)

    # Wait for the thread to finish (until shutdown is called)
    server_thread.join()

# Entry point: starts the server when the script is run directly.
if __name__ == "__main__":
    run_server()
