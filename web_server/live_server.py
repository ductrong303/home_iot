from http.server import BaseHTTPRequestHandler, HTTPServer

# Bind on all network interfaces (0.0.0.0) so other devices on LAN can reach it.
HOST = "0.0.0.0"
PORT = 8080
#-> Tell computer to open ports on all networks interfaces within LAN(local, Wi-Fi, and Ethernet...)
# To access: http://localhost:8080/ or http:// <PC's IP>:8080
latest_data = None

# Simple HTML document.
HTML_PAGE = """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Latest Data</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { font-family: sans-serif; margin: 2em; }
    .box { border: 1px solid #ccc; border-radius: 8px; padding: 1em; max-width: 500px; }
    h1 { font-size: 1.2em; margin-top: 0; }
    pre { background: #f5f5f5; padding: 0.5em; border-radius: 6px; }
    .muted { color: #666; font-size: 0.9em; }
  </style>
</head>
<body>
  <div class="box">
    <h1>ESP/STM Latest Data</h1>
    <div id="data">Loading…</div>
    <p class="muted">Auto-updates every 1 second</p>
  </div>
<script>
async function fetchLatest() {
  try {
    const res = await fetch('/latest');
    const txt = await res.text();
    document.getElementById('data').innerHTML =
      '<pre>' + txt + '</pre>';
  } catch (e) {
    document.getElementById('data').textContent = 'Error fetching data';
  }
}
setInterval(fetchLatest, 1000);
fetchLatest();
</script>
</body>
</html>
"""

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return  # silence default log

    def do_GET(self):
        # called whenever a GET request arrives (devices open webpage)
        global latest_data
        # URL requested
        
        if self.path == "/" or self.path == "/index.html":
            # Example: http://192.168.1.100:8080/ or http://192.168.1.100:8080/index.html
            # Serve the main HTML page
            # Users type the address -> browser sends this request -> sending the HTML dashboard page
            self.send_response(200) # means success
            # Telling browser, data is an HTML page encoded in UTF-8.
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode()) # Sends the actual HTML content
        elif self.path == "/latest":
            # Example: http://192.168.1.100:8080/latest
            # Serve the latest data
            # JS func above auto fetchLatest() -> http://127.0.0.1:8080/latest -> Updates the web page with new values
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8") # plain text, not HTML.
            self.end_headers()
            if latest_data:
                self.wfile.write(latest_data.encode())
            else:
                self.wfile.write(b"No data received yet")
        else:
            self.send_response(404) # Other invalid URL
            self.end_headers()

    def do_POST(self):
        # Handle POST requests (where devices send data)
        global latest_data
        length = int(self.headers.get("Content-Length", 0)) # Read header for content length
        # Read content, decode to utf-8 and replace invalid bytes with char.
        body = self.rfile.read(length).decode("utf-8", errors="replace") 

        latest_data = body.strip() # Remove leading and trailing white space. update latest data
        print(f"From {self.client_address[0]} -> {latest_data}")

        # Reply with code 200 and ok 
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"OK\n")

def main():
    server = HTTPServer((HOST, PORT), Handler)
    print(f"Listening on http://{HOST}:{PORT}")
    try:
        server.serve_forever() # Main loop of the server
        # Each instance lives only for one request (JS/ESP's POST/ Browser) and then is destroyed.
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        server.server_close() # Closes the network socket, freeing the port.

if __name__ == "__main__":
    main()
