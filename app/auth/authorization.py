from fastapi import Depends, HTTPException, status

from app.auth.dependencies import get_current_user 
from app.users.models import User 
from app.users.roles import UserRole


def require_role(required_role: UserRole):

    def role_checker(
            current_user: User = Depends(get_current_user),

    ) -> User:
        
        if current_user.role != require_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        
        return current_user
    

    return role_checker