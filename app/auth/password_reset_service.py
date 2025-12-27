import secrets
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.auth.password_reset_models import PasswordResetToken
from app.users.models import User
from app.core.config import get_settings
from app.core.security import pwd_context, hash_password

logger = logging.getLogger(__name__)
settings = get_settings()


def create_password_reset_token(db: Session, user_id: str) -> str:

    raw_token = secrets.token_urlsafe(32)
    token_hash = pwd_context.hash(raw_token)

    reset_token = PasswordResetToken(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=datetime.now() + timedelta(minutes=30)
    )

    db.add(reset_token)
    db.commit()
    
    logger.info(f"Password reset token created for user {user_id}")
    return raw_token


def verify_and_reset_password(db: Session, token: str, new_password: str) -> None:

    # Get all active reset tokens
    reset_tokens = db.query(PasswordResetToken).all()
    
    if not reset_tokens:
        logger.warning("Password reset attempted with no tokens in database")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )
    
    # Find matching token
    for record in reset_tokens:
        if pwd_context.verify(token, record.token_hash):
            # Check if token is expired
            if record.expires_at < datetime.now():
                logger.warning(f"Expired token used for user {record.user_id}")
                db.delete(record)
                db.commit()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Token has expired"
                )
            
            # Get user and update password
            user = db.get(User, record.user_id)
            if not user:
                logger.error(f"User {record.user_id} not found for password reset")
                db.delete(record)
                db.commit()
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            # Update password
            user.hashed_password = hash_password(new_password)
            
            # Delete used token
            db.delete(record)
            db.commit()
            
            logger.info(f"Password successfully reset for user {user.email}")
            return
    
    # No matching token found
    logger.warning("Invalid password reset token attempted")
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid or expired token"
    )