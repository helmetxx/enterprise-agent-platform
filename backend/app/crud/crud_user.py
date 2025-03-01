from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
import logging

logger = logging.getLogger(__name__)

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        logger.info(f"Executing SQL query for email: {email}")
        result = db.query(User).filter(User.email == email).first()
        logger.info(f"SQL query result: {result}")
        return result

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_superuser=getattr(obj_in, 'is_superuser', False),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        logger.info(f"Attempting authentication for email: {email}")
        
        # 查询用户
        user = self.get_by_email(db, email=email)
        logger.info(f"User query result: {user}")
        
        if not user:
            logger.warning(f"No user found with email: {email}")
            return None
        
        # 验证密码
        if not verify_password(password, user.hashed_password):
            logger.warning(f"Invalid password for user: {email}")
            return None
        
        logger.info(f"Authentication successful for user: {email}")
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser

user = CRUDUser(User) 