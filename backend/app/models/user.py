import sqlalchemy as sa
from sqlalchemy import Table, Column, Integer, String, Boolean, TIMESTAMP, text
from ..core.database import metadata, database
from typing import List, Optional, Dict, Any

# User accounts table
user_accounts = Table(
    "user_accounts",
    metadata,
    Column("user_id", Integer, primary_key=True, autoincrement=True),
    Column("full_name", String(255), nullable=False),
    Column("email", String(255), nullable=False, unique=True),
    Column("password_hash", String(255), nullable=False),
    Column("profile_completed", sa.BOOLEAN, default=False),
    Column("created_at", TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    Column("updated_at", TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
)

class UserModel:
    @staticmethod
    async def find_by_email(email: str) -> List[Dict[str, Any]]:
        """Find user by email"""
        query = user_accounts.select().where(user_accounts.c.email == email)
        result = await database.fetch_all(query)
        return [dict(row) for row in result]
    
    @staticmethod
    async def find_by_id(user_id: int) -> List[Dict[str, Any]]:
        """Find user by ID"""
        query = user_accounts.select().where(user_accounts.c.user_id == user_id)
        result = await database.fetch_all(query)
        return [dict(row) for row in result]
    
    @staticmethod
    async def create_user(full_name: str, email: str, password_hash: str) -> int:
        """Create a new user and return the user ID"""
        query = user_accounts.insert().values(
            full_name=full_name,
            email=email,
            password_hash=password_hash
        )
        result = await database.execute(query)
        return result
    
    @staticmethod
    async def set_profile_completed(user_id: int) -> None:
        """Mark user profile as completed"""
        query = user_accounts.update().where(
            user_accounts.c.user_id == user_id
        ).values(profile_completed=True)
        await database.execute(query)