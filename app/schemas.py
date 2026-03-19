from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# --- TODO SCHEMAS ---
class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None

class TodoCreate(TodoBase):
    pass  # Used when creating a new todo

class Todo(TodoBase):
    id: int
    owner_id: int
    completed: bool
    created_at: datetime

    class Config:
        from_attributes = True  # This allows Pydantic to read SQLAlchemy models

# --- USER SCHEMAS ---
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str  # Only used for registration

class User(UserBase):
    id: int
    is_active: bool
    todos: List[Todo] = []

    class Config:
        from_attributes = True