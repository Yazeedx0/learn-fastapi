from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from uuid import UUID 


from app.auth.models import RefreshToken
from app.core.config import get_settings 



settings = get_settings()


def create_refresh_token(
        db: Session,
        user_id: UUID,

) -> RefreshToken:
    
    token = RefreshToken(
        user_id=user_id,
        expires_at=datetime.now(timezone.utc) 
        + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )

    db.add(token)
    db.commit()
    db.refresh(token)
    return token 