from fastapi import APIRouter, Depends, HTTPException, status
from ..middleware.auth import get_current_user, CurrentUser
from ..models.user import UserModel

router = APIRouter()

@router.get("/")
async def get_me(current_user: CurrentUser = Depends(get_current_user)):
    """
    Get current user information
    """
    try:
        users = await UserModel.find_by_id(current_user.userId)
        
        if not users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user = users[0]
        
        return {
            "account": {
                "user_id": user["user_id"],
                "full_name": user["full_name"],
                "email": user["email"],
                "profile_completed": user["profile_completed"]
            },
            "profileCompleted": bool(user["profile_completed"])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Get me error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user information"
        )