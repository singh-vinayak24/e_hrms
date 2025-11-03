from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database.connection import get_session
from models.models import User
from core.security import get_password_hash, verify_password, create_access_token
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterIn(BaseModel):
    username: str
    email: str | None = None
    password: str
    role: str = "employee"

class LoginIn(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(payload: RegisterIn, session: Session = Depends(get_session)):
    q = select(User).where(User.username == payload.username)
    existing = session.exec(q).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(username=payload.username, email=payload.email, hashed_password=get_password_hash(payload.password), role=payload.role)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"id": user.id, "username": user.username, "role": user.role}

@router.post("/login")
def login(payload: LoginIn, session: Session = Depends(get_session)):
    q = select(User).where(User.username == payload.username)
    user = session.exec(q).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
