import os
import time
import threading
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
from playwright.sync_api import sync_playwright

# Auto-install Playwright browsers on startup if missing
try:
    import playwright

    subprocess.run(["playwright", "install", "chromium"], check=True)
except Exception as e:
    print(f"Browser auto-install notice: {e}")


# --- The Dummy Web Server ---
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Agent is running fine!")
        self.wfile.write(b"Agent is active")

    def log_message(self, format, *args):
        # Suppress routine http logs to keep console clean
        return


def start_web_server():
    server = HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 8080))), DummyHandler)  # type: ignore
    server.serve_forever()


# --- The Agent Logic ---
def run_agent():
    target_url = os.environ.get("TARGET_URL", "https://pers-port.onrender.com/")
    refresh_interval = int(os.environ.get("REFRESH_INTERVAL", 420))

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