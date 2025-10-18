import databases
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import os

# Database URL
DATABASE_URL = settings.DATABASE_URL

# Create database instance
database = databases.Database(DATABASE_URL)

# SQLAlchemy metadata and engine
metadata = sqlalchemy.MetaData()
if "sqlite" in DATABASE_URL:
    engine = sqlalchemy.create_engine(DATABASE_URL.replace("sqlite+aiosqlite", "sqlite"))
else:
    engine = sqlalchemy.create_engine(DATABASE_URL.replace("aiomysql", "pymysql"))

# Base class for models
Base = declarative_base()

# Session maker for sync operations if needed
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)