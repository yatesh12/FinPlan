from fastapi import HTTPException, status
from datetime import datetime, timedelta
from ..models.user import UserModel
from ..models.refresh_token import RefreshTokenModel
from ..utils.tokens import (
    sign_access_token,
    sign_refresh_token,
    verify_refresh_token,
    hash_token,
    compare_token_hash,
    hash_password,
    verify_password
)
from ..schemas.auth import SignupRequest, LoginRequest
from typing import Dict, Any

# Refresh token max age in milliseconds (7 days)
REFRESH_MAX_AGE_MS = 7 * 24 * 3600 * 1000

class AuthService:
    @staticmethod
    async def signup_user(signup_data: SignupRequest) -> Dict[str, Any]:
        """
        Sign up a new user
        """
        # Check if email already exists
        existing_users = await UserModel.find_by_email(signup_data.email)
        if existing_users:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already used"
            )
        
        # Hash password
        password_hash = await hash_password(signup_data.password)
        
        # Create user
        user_id = await UserModel.create_user(
            full_name=signup_data.name,
            email=signup_data.email,
            password_hash=password_hash
        )
        
        return {"userId": user_id}
    
    @staticmethod
    async def login_user(login_data: LoginRequest) -> Dict[str, Any]:
        """
        Login user and return tokens
        """
        # Find user by email
        users = await UserModel.find_by_email(login_data.email)
        if not users:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        user = users[0]
        
        # Verify password
        password_valid = await verify_password(login_data.password, user['password_hash'])
        if not password_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Create tokens
        payload = {"userId": user['user_id'], "email": login_data.email}
        access_token = await sign_access_token(payload)
        refresh_token = await sign_refresh_token(payload)
        
        # Hash and store refresh token
        refresh_hash = await hash_token(refresh_token)
        expires_at = datetime.utcnow() + timedelta(milliseconds=REFRESH_MAX_AGE_MS)
        
        await RefreshTokenModel.insert_token(
            user_id=user['user_id'],
            token_hash=refresh_hash,
            expires_at=expires_at
        )
        
        return {
            "accessToken": access_token,
            "refreshToken": refresh_token,
            "profileCompleted": bool(user['profile_completed']),
            "fullName": user['full_name']
        }
    
    @staticmethod
    async def refresh_tokens(refresh_token: str) -> Dict[str, Any]:
        """
        Refresh access token using refresh token
        """
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No refresh token"
            )
        
        # Verify refresh token
        try:
            payload = await verify_refresh_token(refresh_token)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        user_id = payload.get('userId')
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        # Find matching token in database
        token_rows = await RefreshTokenModel.find_by_user_id_ordered(user_id)
        if not token_rows:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token not recognized"
            )
        
        matched_token = None
        for token_row in token_rows:
            if token_row['revoked']:
                continue
            if token_row['expires_at'] and token_row['expires_at'] < datetime.utcnow():
                continue
            
            # Compare token hash
            if await compare_token_hash(refresh_token, token_row['token_hash']):
                matched_token = token_row
                break
        
        if not matched_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token not recognized"
            )
        
        # Rotate token - revoke old, create new
        new_refresh_token = await sign_refresh_token({
            "userId": payload['userId'],
            "email": payload.get('email', '')
        })
        new_hash = await hash_token(new_refresh_token)
        new_expires_at = datetime.utcnow() + timedelta(milliseconds=REFRESH_MAX_AGE_MS)
        
        # Revoke old token and insert new one
        await RefreshTokenModel.revoke_by_id(matched_token['id'])
        await RefreshTokenModel.insert_token(
            user_id=payload['userId'],
            token_hash=new_hash,
            expires_at=new_expires_at
        )
        
        # Create new access token
        access_token = await sign_access_token({
            "userId": payload['userId'],
            "email": payload.get('email', '')
        })
        
        return {
            "accessToken": access_token,
            "newRefreshToken": new_refresh_token
        }
    
    @staticmethod
    async def logout_user(refresh_token: str) -> None:
        """
        Logout user by revoking all refresh tokens
        """
        if not refresh_token:
            return
        
        try:
            payload = await verify_refresh_token(refresh_token)
            if payload and payload.get('userId'):
                await RefreshTokenModel.revoke_all_for_user(payload['userId'])
        except Exception:
            # Ignore invalid token on logout but still clear cookie
            pass