from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash

# ==========================================
# USER CRUD OPERATIONS
# ==========================================

def get_user(db: Session, user_id: int):
    # .first() returns the first result or None
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    # real encryption
    hashed_password = get_password_hash(user.password)
    
    db_user = models.User(
        username=user.username, 
        email=user.email, 
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ==========================================
# TODO CRUD OPERATIONS
# ==========================================

def get_todos(db: Session, skip: int = 0, limit: int = 100):
    # offset(skip).limit(limit) is how we do Pagination in SQL!
    return db.query(models.Todo).offset(skip).limit(limit).all()

def create_user_todo(db: Session, todo: schemas.TodoCreate, user_id: int):
    # todo.model_dump() converts the Pydantic schema into a Python dictionary.
    # The ** unpacks that dictionary into keyword arguments.
    db_todo = models.Todo(**todo.model_dump(), owner_id=user_id)
    
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo