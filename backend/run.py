"""
AmoebaTronix Smart Support Chatbot - Backend Runner
----------------------------------------------------
Can be run directly from inside the backend/ folder:
python run.py
"""

import sys
import time
import threading
import webbrowser
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent
ROOT_DIR = BACKEND_DIR.parent

sys.path.insert(0, str(BACKEND_DIR))


def open_browser(url: str, delay: float = 1.5):
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

    threading.Thread(target=open_browser, args=(url,), daemon=True).start()

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
