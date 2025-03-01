from fastapi import APIRouter, Depends, HTTPException, Body, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api import deps
from app.core.auth import create_access_token
from app.crud.crud_user import user as user_crud
from app.schemas.user import UserCreate, User
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/register", response_model=User)
async def register(
    request: Request,
    user_in: UserCreate = Body(...),
    db: Session = Depends(deps.get_db)
):
    """
    Create new user.
    """
    logger.info(f"Received registration request")
    logger.info(f"Request method: {request.method}")
    logger.info(f"Request URL: {request.url}")
    logger.info(f"Request headers: {dict(request.headers)}")
    body = await request.body()
    logger.info(f"Request body: {body.decode()}")
    
    try:
        user = user_crud.get_by_email(db, email=user_in.email)
        if user:
            logger.warning(f"User with email {user_in.email} already exists")
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists."
            )
        new_user = user_crud.create(db, obj_in=user_in)
        logger.info(f"User created successfully: {new_user.email}")
        return new_user
    except Exception as e:
        logger.error(f"Error during registration: {str(e)}")
        raise

@router.post("/login")
async def login(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login.
    """
    logger.info(f"Login attempt for username: {form_data.username}")
    
    user = user_crud.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    
    if not user:
        logger.warning(f"Authentication failed for username: {form_data.username}")
        raise HTTPException(
            status_code=400, detail="Incorrect email or password"
        )
    
    logger.info(f"User authenticated successfully: {user.email}")
    access_token = create_access_token(data={"sub": str(user.id)})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    } 