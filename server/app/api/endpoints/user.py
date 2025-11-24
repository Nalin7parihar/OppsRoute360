from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.db_session import get_db
from app.schemas.user import User, UserCreate, UserUpdate
from app.crud.user import user as crud_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[User])
def read_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """Retrieve multiple users."""
    items = crud_user.get_multi(db, skip=skip, limit=limit)
    return items


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Retrieve a single user by ID."""
    db_obj = crud_user.get(db, id=user_id)
    if db_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_obj


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""
    new_obj = crud_user.create(db, obj_in=user)
    return new_obj


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """Update an existing user."""
    db_obj = crud_user.get(db, id=user_id)
    if db_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    updated_obj = crud_user.update(db, db_obj=db_obj, obj_in=user)
    return updated_obj


@router.delete("/{user_id}", response_model=User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user by ID."""
    db_obj = crud_user.get(db, id=user_id)
    if db_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    crud_user.remove(db, id=user_id)
    return db_obj
