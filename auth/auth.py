"""Authentication helpers: password hashing, JWT creation/verification."""
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from jose import JWTError, jwt

from auth.db import get_user_by_email, get_user_by_id, create_user
from auth.models import User, UserPublic

_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-in-production-use-a-long-random-string")
_ALGORITHM = "HS256"
_TOKEN_EXPIRE_DAYS = 30


# ─── Password helpers ─────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


# ─── JWT helpers ──────────────────────────────────────────────────────────────

def create_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=_TOKEN_EXPIRE_DAYS)
    payload = {"sub": user_id, "exp": expire}
    return jwt.encode(payload, _SECRET_KEY, algorithm=_ALGORITHM)


def decode_token(token: str) -> Optional[str]:
    """Returns user_id on success, None on failure."""
    try:
        payload = jwt.decode(token, _SECRET_KEY, algorithms=[_ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None


# ─── Register / Login ─────────────────────────────────────────────────────────

class AuthError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


def register(email: str, password: str, name: str = "") -> tuple[UserPublic, str]:
    """Create a new user. Returns (UserPublic, jwt_token). Raises AuthError on conflict."""
    email = email.lower().strip()
    if not email or "@" not in email:
        raise AuthError("Invalid email address")
    if len(password) < 8:
        raise AuthError("Password must be at least 8 characters")

    existing = get_user_by_email(email)
    if existing:
        raise AuthError("An account with this email already exists", status_code=409)

    pw_hash = hash_password(password)
    user = create_user(email, pw_hash, name=name)
    token = create_token(user.id)
    public = UserPublic(
        id=user.id,
        email=user.email,
        created_at=user.created_at,
        subscription_tier=user.subscription_tier,
        name=user.name,
    )
    return public, token


def login(email: str, password: str) -> tuple[UserPublic, str]:
    """Authenticate. Returns (UserPublic, jwt_token). Raises AuthError on failure."""
    email = email.lower().strip()
    user = get_user_by_email(email)
    if not user or not verify_password(password, user.password_hash):
        raise AuthError("Invalid email or password", status_code=401)

    token = create_token(user.id)
    public = UserPublic(
        id=user.id,
        email=user.email,
        created_at=user.created_at,
        subscription_tier=user.subscription_tier,
        name=user.name,
    )
    return public, token


def get_current_user(token: str) -> Optional[User]:
    """Verify a Bearer token and return the User, or None."""
    user_id = decode_token(token)
    if not user_id:
        return None
    return get_user_by_id(user_id)
