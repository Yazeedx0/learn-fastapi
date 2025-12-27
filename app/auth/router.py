from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.auth.authorization import require_role
from app.users.roles import UserRole
from app.users.service import User
from app.auth.refresh_service import create_refresh_token
from app.auth.models import RefreshToken
from app.core.database import get_db
from app.auth.service import authenticate_user
from app.core.limiter import limiter
from app.auth.schemas import TokenResponse, PasswordResetRequest
from app.auth.password_reset_service import verify_and_reset_password

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Login endpoint that returns access and refresh tokens.
    
    Rate limited to 5 requests per minute per IP address.
    """
    result = authenticate_user(
        db,
        email = form_data.username,
        password=form_data.password
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token, user = result
    
    # Create refresh token in database
    refresh_token_obj = create_refresh_token(db=db, user_id=user.id)
        
    return {
        "access_token": access_token,
        "refresh_token": str(refresh_token_obj.token),
        "token_type": "bearer"
    }

@router.post("/reset-password")
def reset_password(
    reset_data: PasswordResetRequest,
    db: Session = Depends(get_db),
):

    verify_and_reset_password(
        db=db,
        token=reset_data.token,
        new_password=reset_data.new_password
    )
    
    return {"message": "Password successfully updated"}
