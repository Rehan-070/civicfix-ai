import hashlib
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt

from app.database import get_db
from app.config import settings
from app.models.entities import User
from app.schemas.domain import UserRegister, UserLogin, TokenResponse

router = APIRouter()

def hash_password(password: str) -> str:
    return hashlib.sha256(f"salt_civicfix_{password}".encode()).hexdigest()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

@router.post("/register", response_model=TokenResponse)
def register_user(payload: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        full_name=payload.full_name,
        role=payload.role or "CITIZEN"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": user.id, "email": user.email, "role": user.role})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": user.id, "email": user.email, "full_name": user.full_name, "role": user.role}
    }

@router.post("/login", response_model=TokenResponse)
def login_user(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or user.password_hash != hash_password(payload.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": user.id, "email": user.email, "role": user.role})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": user.id, "email": user.email, "full_name": user.full_name, "role": user.role}
    }
