from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..utils.tokens import verify_access_token
from ..models.user import UserModel
from ..schemas.auth import TokenData
from typing import Dict, Any
import jwt

security = HTTPBearer()

class CurrentUser:
    def __init__(self, user_data: Dict[str, Any]):
        self.id = user_data.get('id')
        self.userId = user_data.get('userId') or user_data.get('id')  # Compatibility
        self.email = user_data.get('email')
        self.profileCompleted = user_data.get('profileCompleted', False)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> CurrentUser:
    """
    Dependency to get the current authenticated user
    """
    try:
        # Verify the token
        payload = await verify_access_token(credentials.credentials)
        user_id = payload.get('userId')
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        # Get user from database
        users = await UserModel.find_by_id(user_id)
        if not users:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        user = users[0]
        
        # Create user data
        user_data = {
            'id': user['user_id'],
            'userId': user['user_id'],
            'email': user['email'],
            'profileCompleted': bool(user['profile_completed'])
        }
        
        return CurrentUser(user_data)
        
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token"
        )
    except Exception as e:
        print(f"Auth error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )