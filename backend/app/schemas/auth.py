from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import Optional, Self

class SignupRequest(BaseModel):
    name: Optional[str] = None
    fullName: Optional[str] = None
    email: EmailStr
    password: str
    
    @model_validator(mode='after')
    def set_name_from_full_name(self) -> Self:
        # Use 'name' if provided, otherwise use 'fullName'
        if not self.name and self.fullName:
            self.name = self.fullName
        elif not self.name and not self.fullName:
            raise ValueError('Either name or fullName must be provided')
        return self
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class SignupResponse(BaseModel):
    message: str
    user: dict

class LoginResponse(BaseModel):
    accessToken: str
    profileCompleted: bool
    fullName: str

class RefreshResponse(BaseModel):
    accessToken: str

class LogoutResponse(BaseModel):
    message: str

class TokenData(BaseModel):
    userId: int
    email: str