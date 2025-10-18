import sqlalchemy as sa
from sqlalchemy import Table, Column, Integer, String, DECIMAL, Text, Enum, TIMESTAMP, text, ForeignKey
from ..core.database import metadata, database
from typing import List, Optional, Dict, Any

# User profiles table
user_profiles = Table(
    "user_profiles",
    metadata,
    Column("profile_id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey("user_accounts.user_id", ondelete="CASCADE"), nullable=False, unique=True),
    Column("age", Integer),
    Column("income", DECIMAL(15, 2)),
    Column("savings", DECIMAL(15, 2)),
    Column("expenses", DECIMAL(15, 2)),
    Column("financial_goals", Text),
    Column("risk_tolerance", Enum("low", "medium", "high", name="risk_tolerance_enum"), default="medium"),
    Column("investment_experience", Enum("beginner", "intermediate", "advanced", name="investment_experience_enum"), default="beginner"),
    Column("created_at", TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    Column("updated_at", TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
)

# Financial goals table
financial_goals = Table(
    "financial_goals",
    metadata,
    Column("goal_id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey("user_accounts.user_id", ondelete="CASCADE"), nullable=False),
    Column("goal_name", String(255), nullable=False),
    Column("target_amount", DECIMAL(15, 2), nullable=False),
    Column("current_amount", DECIMAL(15, 2), default=0),
    Column("target_date", sa.Date),
    Column("priority", Enum("low", "medium", "high", name="priority_enum"), default="medium"),
    Column("status", Enum("active", "completed", "paused", name="status_enum"), default="active"),
    Column("created_at", TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    Column("updated_at", TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
)

# Budget categories table
budget_categories = Table(
    "budget_categories",
    metadata,
    Column("category_id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey("user_accounts.user_id", ondelete="CASCADE"), nullable=False),
    Column("category_name", String(100), nullable=False),
    Column("budgeted_amount", DECIMAL(15, 2), nullable=False),
    Column("spent_amount", DECIMAL(15, 2), default=0),
    Column("category_type", Enum("income", "expense", name="category_type_enum"), nullable=False),
    Column("created_at", TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    Column("updated_at", TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
)

# Transactions table
transactions = Table(
    "transactions",
    metadata,
    Column("transaction_id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey("user_accounts.user_id", ondelete="CASCADE"), nullable=False),
    Column("category_id", Integer, ForeignKey("budget_categories.category_id", ondelete="SET NULL")),
    Column("amount", DECIMAL(15, 2), nullable=False),
    Column("description", String(255)),
    Column("transaction_type", Enum("income", "expense", name="transaction_type_enum"), nullable=False),
    Column("transaction_date", sa.Date, nullable=False),
    Column("created_at", TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
)

class ProfileModel:
    @staticmethod
    async def get_profile_by_user_id(user_id: int) -> Optional[Dict[str, Any]]:
        """Get user profile by user ID"""
        query = user_profiles.select().where(user_profiles.c.user_id == user_id)
        result = await database.fetch_one(query)
        return dict(result) if result else None
    
    @staticmethod
    async def create_or_update_profile(user_id: int, profile_data: Dict[str, Any]) -> None:
        """Create or update user profile"""
        # Check if profile exists
        existing = await ProfileModel.get_profile_by_user_id(user_id)
        
        if existing:
            # Update existing profile
            query = user_profiles.update().where(
                user_profiles.c.user_id == user_id
            ).values(**profile_data)
        else:
            # Create new profile
            profile_data['user_id'] = user_id
            query = user_profiles.insert().values(**profile_data)
        
        await database.execute(query)
    
    @staticmethod
    async def get_financial_goals(user_id: int) -> List[Dict[str, Any]]:
        """Get financial goals for user"""
        query = financial_goals.select().where(financial_goals.c.user_id == user_id)
        result = await database.fetch_all(query)
        return [dict(row) for row in result]
    
    @staticmethod
    async def create_financial_goal(user_id: int, goal_data: Dict[str, Any]) -> int:
        """Create a new financial goal"""
        goal_data['user_id'] = user_id
        query = financial_goals.insert().values(**goal_data)
        result = await database.execute(query)
        return result