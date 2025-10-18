import sqlalchemy as sa
from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, TIMESTAMP, text, ForeignKey
from ..core.database import metadata, database
from typing import List, Optional, Dict, Any
from datetime import datetime

# Refresh tokens table
refresh_tokens = Table(
    "refresh_tokens",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey("user_accounts.user_id", ondelete="CASCADE"), nullable=False),
    Column("token_hash", String(255), nullable=False),
    Column("expires_at", DateTime, nullable=False),
    Column("revoked", sa.BOOLEAN, default=False),
    Column("created_at", TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
)

class RefreshTokenModel:
    @staticmethod
    async def insert_token(user_id: int, token_hash: str, expires_at: datetime) -> int:
        """Insert a new refresh token"""
        query = refresh_tokens.insert().values(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at
        )
        result = await database.execute(query)
        return result
    
    @staticmethod
    async def find_by_user_id_ordered(user_id: int) -> List[Dict[str, Any]]:
        """Find refresh tokens for user, ordered by created_at desc"""
        query = refresh_tokens.select().where(
            refresh_tokens.c.user_id == user_id
        ).order_by(refresh_tokens.c.created_at.desc())
        result = await database.fetch_all(query)
        return [dict(row) for row in result]
    
    @staticmethod
    async def revoke_by_id(token_id: int) -> None:
        """Revoke a refresh token by ID"""
        query = refresh_tokens.update().where(
            refresh_tokens.c.id == token_id
        ).values(revoked=True)
        await database.execute(query)
    
    @staticmethod
    async def revoke_all_for_user(user_id: int) -> None:
        """Revoke all refresh tokens for a user"""
        query = refresh_tokens.update().where(
            refresh_tokens.c.user_id == user_id
        ).values(revoked=True)
        await database.execute(query)