"""
Justice AI - Unified Production Process Orchestrator
Launches and monitors both the Backend REST API (:5000) and Frontend Client (:3000).
Usage: python run_all.py
"""

import subprocess
import sys
import time
import os
import signal

def main():
    print("=" * 65)
    print("  ⚖️  JUSTICE AI - GLOBAL LEGAL INTELLIGENCE SUITE")
    print("  Starting Decoupled Production Environment...")
    print("=" * 65)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    python_exe = sys.executable

    # 1. Start Dedicated Backend REST API (Port 5000)
    print("\n[1/2] Launching Backend REST API Server on http://localhost:5000...")
    backend_proc = subprocess.Popen(
        [python_exe, "backend_server.py"],
        cwd=base_dir
    )

    # Allow backend to bind socket
    time.sleep(1.5)

    # 2. Start Dedicated Frontend Static Client (Port 3000)
    print("[2/2] Launching Frontend Web Interface on http://localhost:3000...")
    frontend_proc = subprocess.Popen(
        [python_exe, "frontend_server.py"],
        cwd=base_dir
    )

    print("\n" + "=" * 65)
    print("  ✅ All Services Successfully Deployed and Active!")
    print("  • Frontend Web Client : http://localhost:3000")
    print("  • Backend REST API    : http://localhost:5000/api/health")
    print("  • API Chat Endpoint   : http://localhost:5000/api/chat")
    print("=" * 65)
    print("  Press Ctrl+C to safely terminate all servers.\n")

    def shutdown(signum, frame):
        print("\n[Shutdown] Terminating servers gracefully...")
        try:
            backend_proc.terminate()
            frontend_proc.terminate()
            backend_proc.wait(timeout=3)
            frontend_proc.wait(timeout=3)
        except Exception:
            backend_proc.kill()
            frontend_proc.kill()
        print("[Shutdown] Servers stopped.")
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, shutdown)

    try:
        while True:
            time.sleep(1)
            if backend_proc.poll() is not None:
                print("[Warning] Backend process exited unexpectedly.")
                break
            if frontend_proc.poll() is not None:
                print("[Warning] Frontend process exited unexpectedly.")
                break
    except KeyboardInterrupt:
        shutdown(None, None)


if __name__ == "__main__":
    main()
