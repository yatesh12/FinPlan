import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Dict, Any
from ..core.config import settings

def parse_time_string(time_str: str) -> int:
    """Parse time string like '900s' or '7d' to seconds"""
    if time_str.endswith('s'):
        return int(time_str[:-1])
    elif time_str.endswith('m'):
        return int(time_str[:-1]) * 60
    elif time_str.endswith('h'):
        return int(time_str[:-1]) * 3600
    elif time_str.endswith('d'):
        return int(time_str[:-1]) * 24 * 3600
    else:
        return int(time_str)

async def sign_access_token(payload: Dict[str, Any]) -> str:
    """Sign an access token"""
    expires_in_seconds = parse_time_string(settings.ACCESS_TOKEN_EXPIRES_IN)
    exp = datetime.utcnow() + timedelta(seconds=expires_in_seconds)
    payload_with_exp = {**payload, "exp": exp, "type": "access"}
    return jwt.encode(payload_with_exp, settings.JWT_ACCESS_SECRET, algorithm="HS256")

async def sign_refresh_token(payload: Dict[str, Any]) -> str:
    """Sign a refresh token"""
    expires_in_seconds = parse_time_string(settings.REFRESH_TOKEN_EXPIRES_IN)
    exp = datetime.utcnow() + timedelta(seconds=expires_in_seconds)
    payload_with_exp = {**payload, "exp": exp, "type": "refresh"}
    return jwt.encode(payload_with_exp, settings.JWT_REFRESH_SECRET, algorithm="HS256")

async def verify_access_token(token: str) -> Dict[str, Any]:
    """Verify and decode access token"""
    try:
        payload = jwt.decode(token, settings.JWT_ACCESS_SECRET, algorithms=["HS256"])
        if payload.get("type") != "access":
            raise jwt.InvalidTokenError("Invalid token type")
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.InvalidTokenError("Token expired")
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError("Invalid token")

async def verify_refresh_token(token: str) -> Dict[str, Any]:
    """Verify and decode refresh token"""
    try:
        payload = jwt.decode(token, settings.JWT_REFRESH_SECRET, algorithms=["HS256"])
        if payload.get("type") != "refresh":
            raise jwt.InvalidTokenError("Invalid token type")
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.InvalidTokenError("Token expired")
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError("Invalid token")

async def hash_token(token: str) -> str:
    """Hash a token for storage"""
    return bcrypt.hashpw(token.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

async def compare_token_hash(token: str, hashed: str) -> bool:
    """Compare token with its hash"""
    return bcrypt.checkpw(token.encode('utf-8'), hashed.encode('utf-8'))

async def hash_password(password: str) -> str:
    """Hash a password"""
    salt_rounds = settings.BCRYPT_SALT_ROUNDS
    salt = bcrypt.gensalt(rounds=salt_rounds)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

async def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))