from fastapi import APIRouter, Depends, HTTPException, status
from ..middleware.auth import get_current_user, CurrentUser
from ..models.profile import ProfileModel
from ..models.user import UserModel
from typing import Dict, Any
from pydantic import BaseModel

router = APIRouter()

class ProfileData(BaseModel):
    class Config:
        extra = "allow"  # Allow additional fields

@router.post("/")
async def upsert_profile(
    profile_data: ProfileData,
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Create or update user profile
    """
    try:
        # Valid column names for user_profiles table
        valid_columns = {
            'age', 'income', 'savings', 'expenses', 'financial_goals', 
            'risk_tolerance', 'investment_experience'
        }
        
        # Field mappings from frontend to database
        field_mappings = {
            'monthly_expenses': 'expenses',
            'monthly_income': 'income',
            'monthly_savings_amt': 'savings',
            'annual_income': 'income',
            'experience_level': 'investment_experience',
            'risk_level': 'risk_tolerance',
            'risk_comfort_level': 'risk_tolerance',  # Added mapping for profile tab
            'goals': 'financial_goals',
            'primary_goal': 'financial_goals',
            'pref_risk_tolerance': 'risk_tolerance',
            'investment_exp': 'investment_experience'
        }
        
        # Filter and map the data
        raw_data = profile_data.dict()
        filtered_data = {}
        
        for key, value in raw_data.items():
            # Skip None values
            if value is None:
                continue
                
            # Map field names
            db_key = field_mappings.get(key, key)
            
            # Only include valid columns
            if db_key in valid_columns:
                filtered_data[db_key] = value
        
        print(f"Filtered profile data: {filtered_data}")
        
        # Create or update profile
        await ProfileModel.create_or_update_profile(current_user.userId, filtered_data)
        
        # Mark profile as completed
        await UserModel.set_profile_completed(current_user.userId)
        
        return {"message": "Profile updated successfully", "success": True}
        
    except Exception as e:
        print(f"Profile upsert error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )

@router.get("/")
async def get_profile(current_user: CurrentUser = Depends(get_current_user)):
    """
    Get user profile
    """
    try:
        profile = await ProfileModel.get_profile_by_user_id(current_user.userId)
        
        # If no profile exists, return empty profile structure instead of None
        if profile is None:
            profile = {
                "age": None,
                "income": None,
                "savings": None,
                "expenses": None,
                "financial_goals": None,
                "risk_tolerance": None,
                "investment_experience": None
            }
        
        return {"success": True, "profile": profile}
        
    except Exception as e:
        print(f"Get profile error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get profile"
        )