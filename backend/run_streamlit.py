#!/usr/bin/env python3
import subprocess
import sys
import os

def run_streamlit():
    """Run Streamlit with configuration optimized for iframe embedding"""
    
    # Change to the backend directory
    os.chdir('/Users/adityakhalkar/FinPlanAI/backend')
    
    # Streamlit configuration for iframe embedding
    cmd = [
        sys.executable, '-m', 'streamlit', 'run', 'streamlit_app.py',
        '--server.port=8501',
        '--server.headless=true',
        '--server.enableCORS=false',
        '--server.enableXsrfProtection=false',
        '--browser.gatherUsageStats=false'
    ]
    
    print("🚀 Starting Streamlit app optimized for iframe embedding...")
    print(f"📍 URL: http://localhost:8501")
    print("🔧 Configuration: CORS disabled, XSRF protection disabled")
    print("⚡ Ready for embedding in React app!")
    print("-" * 50)
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n🛑 Streamlit app stopped.")
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")

if __name__ == "__main__":
    run_streamlit()