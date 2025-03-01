from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
import uuid

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(
        id=str(uuid.uuid4()),  # 生成 UUID
        email=user.email,
        username=user.username
    )
    db_user.password = user.password  # 这里会自动进行密码哈希
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not user.verify_password(password):
        return None
    return user 