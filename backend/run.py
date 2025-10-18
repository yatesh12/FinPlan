from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

# Create FastAPI app without database lifespan for testing
app = FastAPI(
    title="FinPlanAI Backend",
    description="Financial Planning API built with FastAPI",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With", "Accept"],
)

# Health check
@app.get("/health")
async def health_check():
    return {"ok": True, "status": "healthy", "message": "FastAPI backend is running"}

# Test endpoint
@app.get("/")
async def root():
    return {"message": "FinPlanAI FastAPI Backend is running!", "version": "2.0.0"}

if __name__ == "__main__":
    uvicorn.run("run:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)