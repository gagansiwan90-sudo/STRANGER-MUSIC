#!/usr/bin/env python3
print("🌐 Starting HTTP Server on 0.0.0.0:8080...")
import os, threading, time
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Stranger Music OK')
    def log_message(self, *args): pass

server = HTTPServer(('0.0.0.0', 8080), Handler)
print("✅ Port 8080 BOUND SUCCESS")
threading.Thread(target=server.serve_forever, daemon=True).start()

# Original bot code
time.sleep(10)  # Wait for port detection
exec(open('original_main.py').read())  # Run your original main.py
