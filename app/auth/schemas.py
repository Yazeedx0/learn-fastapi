from pydantic import BaseModel, field_validator, Field
import re


class TokenResponse(BaseModel):
    """Response model for login endpoint"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token payload data"""
    sub: str | None = None
    exp: int | None = None
    type: str | None = None


class PasswordResetRequest(BaseModel):
    """Schema for password reset request"""
    token: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8, max_length=100)
    
    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v: str) -> str:

        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v
