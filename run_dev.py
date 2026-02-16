#!/usr/bin/env python3
"""
Development server runner for Smart Crop Advisory System
This script starts both backend and frontend development servers.
"""

import subprocess
import sys
import time
import signal
import os
from pathlib import Path


def run_command(command, cwd=None, shell=True):
    """Run a command in a subprocess"""
    return subprocess.Popen(
        command,
        cwd=cwd,
        shell=shell,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )


def main():
    """Main function to start development servers"""
    print("🌾 Starting Smart Crop Advisory System Development Servers")
    print("=" * 60)
    
    processes = []
    
    try:
        # Start backend server
        print("🚀 Starting backend server...")
        if os.name == 'nt':  # Windows
            backend_cmd = "backend\\venv\\Scripts\\python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
        else:  # Unix/Linux/macOS
            backend_cmd = "backend/venv/bin/python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
        
        backend_process = run_command(backend_cmd, cwd="backend")
        processes.append(("Backend", backend_process))
        
        # Wait a moment for backend to start
        time.sleep(3)
        
        # Start frontend server
        print("🚀 Starting frontend server...")
        frontend_process = run_command("npm start", cwd="frontend")
        processes.append(("Frontend", frontend_process))
        
        print("\n✅ Development servers started!")
        print("\n📱 Access the application:")
        print("   Frontend: http://localhost:3000")
        print("   Backend API: http://localhost:8000")
        print("   API Docs: http://localhost:8000/docs")
        print("\n🛑 Press Ctrl+C to stop all servers")
        
        # Monitor processes
        while True:
            time.sleep(1)
            for name, process in processes:
                if process.poll() is not None:
                    print(f"\n❌ {name} server stopped unexpectedly")
                    return
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping development servers...")
        
        # Stop all processes
        for name, process in processes:
            print(f"Stopping {name} server...")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        
        print("✅ All servers stopped")


if __name__ == "__main__":
    main()
