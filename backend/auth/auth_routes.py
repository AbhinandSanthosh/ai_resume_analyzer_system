from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database.db import get_db
from backend.models.user_model import User

from backend.auth.auth_handler import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter()


class RegisterRequest(BaseModel):

    username: str
    email: str
    password: str


class LoginRequest(BaseModel):

    email: str
    password: str


@router.post("/register")
def register_user(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == request.email
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_user = User(

        username=request.username,

        email=request.email,

        password=hash_password(
            request.password
        )
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {

        "message":
        "User registered successfully"
    }


@router.post("/login")
def login_user(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == request.email
    ).first()

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email"
        )

    if not verify_password(
        request.password,
        user.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    token = create_access_token(

        data={
            "sub": user.email,
            "role": user.role
        }
    )

    return {

        "access_token": token,

        "token_type": "bearer"
    }