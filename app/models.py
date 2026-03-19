from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base  # Note the '.' - it means 'from current package'

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationship: One user can have many todos
    # 'back_populates' creates a link to the Todo class
    todos = relationship("Todo", back_populates="owner")

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True, nullable=False)
    description = Column(String(255))
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Foreign Key: Links a todo to a specific user id
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Relationship: Link back to the User object
    owner = relationship("User", back_populates="todos")