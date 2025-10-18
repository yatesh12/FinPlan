from fastapi import Response
from ..core.config import settings

def set_refresh_cookie(response: Response, refresh_token: str, max_age_ms: int) -> None:
    """Set refresh token cookie"""
    max_age_seconds = max_age_ms // 1000
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=max_age_seconds,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE
    )

def clear_refresh_cookie(response: Response) -> None:
    """Clear refresh token cookie"""
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE
    )