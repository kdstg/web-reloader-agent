import os
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from playwright.sync_api import sync_playwright


# --- The Dummy Web Server ---
class DummyHandler(BaseHTTPRequestHandler):
    def do_get(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Agent is running!")


def start_web_server():
    server = HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 8080))), DummyHandler) # type: ignore
    server.serve_forever()


# --- The Agent Logic ---
def run_agent():
    target_url = os.environ.get("TARGET_URL", "https://pers-port.onrender.com/")
    refresh_interval = int(os.environ.get("REFRESH_INTERVAL", 300))

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page()
        while True:
            page.goto(target_url)
            time.sleep(refresh_interval)


# --- Start Both ---
if __name__ == "__main__":
    # Start web server in background thread
    threading.Thread(target=start_web_server, daemon=True).start()
    # Run agent in main thread
    run_agent()