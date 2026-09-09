"""
AmoebaTronix Smart Support Chatbot - Unified Runner
----------------------------------------------------
Starts both the FastAPI Backend API and Frontend UI in a single run.
Serves on: http://127.0.0.1:8000
"""

import os
import sys
import time
import threading
import webbrowser
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"

# Ensure backend folder is in Python search path
sys.path.insert(0, str(BACKEND_DIR))


def open_browser(url: str, delay: float = 1.5):
    """Wait for server to start, then open the frontend UI in default browser."""
    time.sleep(delay)
    print(f"\n[UI] Opening browser at {url} ...")
    webbrowser.open(url)


def main():
    host = "127.0.0.1"
    port = 8000
    url = f"http://{host}:{port}"

    print("=" * 65)
    print("  🚀 AmoebaTronix Smart Support Chatbot")
    print("  Unified Server: FastAPI + RAG + Frontend UI")
    print(f"  URL: {url}")
    print("  API Docs: " + f"{url}/docs")
    print("  Press CTRL+C to stop.")
    print("=" * 65 + "\n")

    # Launch browser automatically
    browser_thread = threading.Thread(target=open_browser, args=(url,), daemon=True)
    browser_thread.start()

    # Import uvicorn and run FastAPI server
    try:
        import uvicorn
        uvicorn.run(
            "app:app",
            host=host,
            port=port,
            reload=True,
            app_dir=str(BACKEND_DIR),
            reload_dirs=[str(BACKEND_DIR), str(ROOT_DIR / "frontend")]
        )
    except KeyboardInterrupt:
        print("\n[Server] Shutting down gracefully...")


if __name__ == "__main__":
    main()
