from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastapi import HTTPException

from backend.database.db import get_db
from backend.models.user_model import User
from backend.schemas.user_schema import UserCreate

router = APIRouter()


@router.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.email == request.email
        ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        name=user.name,
        email=user.email
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "message": "user created successfully",
        "user": new_user.name
    }


@router.get("/users")
def get_users(db: Session = Depends(get_db)):

    users = db.query(User).all()

    return users


@router.delete("/users")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return {"error": "user not found"}

    db.delete(user)

    db.commit()

    return {
        "message": "user deleted successfully"
    }