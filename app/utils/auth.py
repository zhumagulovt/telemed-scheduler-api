from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        bytes(plain_password, "utf-8"), bytes(hashed_password, encoding="utf-8")
    )


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(bytes(password, encoding="utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
