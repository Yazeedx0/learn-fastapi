from pydantic import BaseModel


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
