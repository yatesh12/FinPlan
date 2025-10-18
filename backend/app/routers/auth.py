from fastapi import APIRouter, HTTPException, status, Response, Request, Depends
from fastapi.responses import JSONResponse
from ..schemas.auth import (
    SignupRequest, 
    LoginRequest, 
    SignupResponse, 
    LoginResponse, 
    RefreshResponse, 
    LogoutResponse
)
from ..services.auth_service import AuthService, REFRESH_MAX_AGE_MS
from ..utils.cookies import set_refresh_cookie, clear_refresh_cookie
from pydantic import ValidationError

router = APIRouter()

@router.post("/signup", response_model=SignupResponse)
async def signup(signup_data: SignupRequest):
    """
    User signup endpoint
    """
    try:
        print(f"Signup request: {signup_data}")
        
        result = await AuthService.signup_user(signup_data)
        
        return SignupResponse(
            message="Signup successful",
            user={"userId": result["userId"]}
        )
        
    except HTTPException:
        raise
    except ValidationError as e:
        print(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e.errors()[0]['msg']) if e.errors() else "Validation failed"
        )
    except Exception as e:
        print(f"Signup unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest, response: Response):
    """
    User login endpoint
    """
    try:
        result = await AuthService.login_user(login_data)
        
        # Set refresh token cookie
        set_refresh_cookie(response, result["refreshToken"], REFRESH_MAX_AGE_MS)
        
        return LoginResponse(
            accessToken=result["accessToken"],
            profileCompleted=result["profileCompleted"],
            fullName=result["fullName"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

@router.post("/refresh", response_model=RefreshResponse)
async def refresh_token(request: Request, response: Response):
    """
    Refresh access token endpoint
    """
    try:
        # Get refresh token from cookie
        refresh_token = request.cookies.get("refresh_token")
        
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No refresh token"
            )
        
        result = await AuthService.refresh_tokens(refresh_token)
        
        # Set new refresh token cookie
        set_refresh_cookie(response, result["newRefreshToken"], REFRESH_MAX_AGE_MS)
        
        return RefreshResponse(accessToken=result["accessToken"])
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

@router.post("/logout", response_model=LogoutResponse)
async def logout(request: Request, response: Response):
    """
    User logout endpoint
    """
    try:
        # Get refresh token from cookie
        refresh_token = request.cookies.get("refresh_token")
        
        # Logout user (revoke tokens)
        await AuthService.logout_user(refresh_token)
        
        # Clear refresh token cookie
        clear_refresh_cookie(response)
        
        return LogoutResponse(message="Logged out")
        
    except Exception as e:
        print(f"Logout error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )