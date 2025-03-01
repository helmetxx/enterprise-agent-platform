from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.api import deps

router = APIRouter()

@router.get("/me", response_model=schemas.User)
def read_user_me(
    current_user: schemas.User = Depends(deps.get_current_user)
):
    """
    Get current user.
    """
    return current_user

@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: int,
    current_user: schemas.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user

@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    password: str = None,
    full_name: str = None,
    current_user: schemas.User = Depends(deps.get_current_user),
):
    """
    Update own user.
    """
    current_user_data = schemas.UserUpdate(
        password=password,
        full_name=full_name,
        email=current_user.email,
    )
    user = crud.user.update(db, db_obj=current_user, obj_in=current_user_data)
    return user 