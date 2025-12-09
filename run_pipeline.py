import subprocess
import sys
import os
import time
import signal

def run_background(cmd):
    print(f"\n🔥 Starting (background): {cmd}\n")
    return subprocess.Popen(cmd, shell=True)

def run_foreground(cmd):
    print(f"\n🚀 Running (foreground): {cmd}\n")
    process = subprocess.Popen(cmd, shell=True)
    process.communicate()

    if process.returncode != 0:
        print(f"\n❌ Command failed: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    # 1) Prepare database folder
    os.makedirs("data", exist_ok=True)

    print("\n📁 data/ folder ensured.\n")

    # 2) Start Streamlit UI in background
    streamlit_process = run_background("streamlit run frontend/app.py")


    # Optional: give time for Streamlit to start
    time.sleep(2)

    # 3) Start FastAPI server (foreground)
    try:
        run_foreground("uvicorn backend.main:app --reload")

    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested. Cleaning up...")

    finally:
        # Kill streamlit process on exit
        streamlit_process.terminate()
        try:
            streamlit_process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            streamlit_process.kill()

        print("\n✨ All services stopped.\n")
