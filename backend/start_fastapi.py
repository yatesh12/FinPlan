#!/usr/bin/env python3
"""
FastAPI Backend Startup Script
Ensures proper environment setup and starts the server
"""

import os
import sys
import subprocess

def main():
    # Ensure we're in the correct directory
    os.chdir('/Users/adityakhalkar/FinPlanAI/backend')
    
    # Check if virtual environment exists
    venv_python = './venv/bin/python'
    if not os.path.exists(venv_python):
        print("❌ Virtual environment not found!")
        print("Please run: python -m venv venv && source venv/bin/activate && pip install -r requirements.txt")
        return 1
    
    # Test imports
    print("🔍 Testing imports...")
    result = subprocess.run([venv_python, 'test_imports.py'], capture_output=True, text=True)
    
    if result.returncode != 0:
        print("❌ Import test failed:")
        print(result.stdout)
        print(result.stderr)
        return 1
    
    print("✅ All imports successful!")
    
    # Start FastAPI server
    print("🚀 Starting FastAPI server on http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    
    try:
        # Use the virtual environment python directly
        subprocess.run([
            venv_python, 
            '-m', 'uvicorn', 
            'main:app', 
            '--host', '0.0.0.0', 
            '--port', '8000', 
            '--reload'
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())