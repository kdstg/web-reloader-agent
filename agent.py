import os
import time
from playwright.sync_api import sync_playwright

TARGET_URL = os.environ.get("TARGET_URL", "")
REFRESH_INTERVAL = int(os.environ.get("REFRESH_INTERVAL", 420))

def run_cloud_agent():
    print(f"[Agent Initiating] Target:{TARGET_URL}")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args = [
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "disable-gpu",
            ]
        )
        context = browser.new_context()
        page = context.new_page()

        print("[Agent Ready] Cloud browser launched successfully!")

        try:
            while True:
                print(f"[{time.strftime('%H:%M:%S')}] Refreshing target page...")
                page.goto(TARGET_URL, wait_until="networkidle")
                print(f"[{time.strftime('%H:%M:%S')}] Page loaded successfully! Waiting for {REFRESH_INTERVAL} seconds...")

                time.sleep(REFRESH_INTERVAL)

        except Exception as e:
            print(f"[Error Encountered]: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run_cloud_agent()