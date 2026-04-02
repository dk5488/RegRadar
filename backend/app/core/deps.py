"""
RegRadar — Auth Dependencies
FastAPI dependencies for JWT-based authentication and role-based access control.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.models import User
from app.models.enums import UserRole

# Bearer token extractor — looks for "Authorization: Bearer <token>"
bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Core auth dependency.
    Extracts JWT from Authorization header, decodes it,
    and returns the authenticated User from the database.

    Raises 401 if:
      - No token provided
      - Token is invalid / expired
      - User not found in database
      - User account is deactivated
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated",
        )

    return user


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> Optional[User]:
    """
    Optional auth — returns None if no token is provided,
    but validates the token if one is present.
    Useful for endpoints that behave differently for logged-in vs anonymous users.
    """
    if credentials is None:
        return None
    return await get_current_user(credentials, db)


class RoleChecker:
    """
    Dependency factory for role-based access control.

    Usage in a route:
        require_ca = RoleChecker([UserRole.CA_REVIEWER, UserRole.CA_FIRM_ADMIN])

        @router.get("/review", dependencies=[Depends(require_ca)])
        async def review_doc(...):
            ...

    Or inject the user directly:
        async def review_doc(user: User = Depends(require_ca)):
            ...
    """

    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles

    async def __call__(
        self, current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires one of: {', '.join(r.value for r in self.allowed_roles)}",
            )
        return current_user


# ── Pre-built role guards ─────────────────────────────────────────────

# Any authenticated user
require_authenticated = get_current_user

# Admin only
require_admin = RoleChecker([UserRole.ADMIN])

# CA roles (firm admin + reviewer)
require_ca = RoleChecker([UserRole.CA_FIRM_ADMIN, UserRole.CA_REVIEWER, UserRole.ADMIN])

# CA firm admin or platform admin
require_ca_admin = RoleChecker([UserRole.CA_FIRM_ADMIN, UserRole.ADMIN])

# MSME owner (or admin)
require_msme_or_admin = RoleChecker([UserRole.MSME_OWNER, UserRole.ADMIN])

# Anyone with a CA or MSME role (basically all authenticated non-admin)
require_any_role = RoleChecker([
    UserRole.ADMIN,
    UserRole.CA_FIRM_ADMIN,
    UserRole.CA_REVIEWER,
    UserRole.MSME_OWNER,
])
