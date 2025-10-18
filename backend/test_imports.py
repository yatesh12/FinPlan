#!/usr/bin/env python3
"""
Test script to verify all imports work correctly
"""

try:
    print("Testing imports...")
    
    # Test basic imports
    import fastapi
    print("✓ fastapi imported")
    
    import uvicorn
    print("✓ uvicorn imported")
    
    import databases
    print("✓ databases imported")
    
    import aiosqlite
    print("✓ aiosqlite imported")
    
    import sqlalchemy
    print("✓ sqlalchemy imported")
    
    # Test app imports
    from app.core.config import settings
    print(f"✓ settings imported - USE_SQLITE: {settings.USE_SQLITE}")
    
    from app.core.database import database, DATABASE_URL
    print(f"✓ database imported - URL: {DATABASE_URL}")
    
    print("\n✅ All imports successful!")
    print("You can now run the FastAPI backend.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")