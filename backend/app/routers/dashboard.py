from fastapi import APIRouter, Depends, HTTPException, status
from ..middleware.auth import get_current_user, CurrentUser
from ..models.profile import ProfileModel
from typing import Dict, Any

router = APIRouter()

@router.get("/{user_id}")
async def get_dashboard_data(
    user_id: int, 
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Get dashboard data by user ID (must match logged-in user)
    """
    try:
        # Prevent access to other users' data
        if user_id != current_user.userId:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized access"
            )
        
        # Get profile data for the user
        profile_data = await ProfileModel.get_profile_by_user_id(user_id)
        
        if not profile_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No dashboard data found for this user."
            )
        
        return profile_data
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Dashboard error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get dashboard data"
        )

@router.get("/me")
async def get_current_user_dashboard(
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Get dashboard data for current logged-in user
    """
    try:
        # Get profile data for the current user
        profile_data = await ProfileModel.get_profile_by_user_id(current_user.userId)
        
        if not profile_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No dashboard data found for current user."
            )
        
        return profile_data
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Dashboard error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get dashboard data"
        )