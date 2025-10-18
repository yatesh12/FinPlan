from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv

from app.core.config import settings
from app.core.database import database, engine, metadata
from app.routers import auth, profile, me, dashboard, portfolio
from app.middleware.auth import get_current_user

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await database.connect()
    yield
    # Shutdown
    await database.disconnect()

app = FastAPI(
    title="FinPlanAI Backend",
    description="Financial Planning API built with FastAPI",
    version="2.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With", "Accept"],
)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Root endpoint
@app.get("/")
async def root():
    return {"message": "FinPlanAI FastAPI Backend", "version": "2.0.0", "status": "running"}

# Routes
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(profile.router, prefix="/api/profile", tags=["profile"], dependencies=[Depends(get_current_user)])
app.include_router(me.router, prefix="/api/me", tags=["user"], dependencies=[Depends(get_current_user)])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"], dependencies=[Depends(get_current_user)])
app.include_router(portfolio.router, prefix="/api/portfolio", tags=["portfolio"], dependencies=[Depends(get_current_user)])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)