from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext

# 1. JWT Configuration
# In production, NEVER hardcode this. Read it from a .env file!
# You can generate a strong key in your terminal using: openssl rand -hex 32
SECRET_KEY = "your_super_secret_key_please_change_this_later"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 2. Password Hashing Configuration
# This tells passlib to use the bcrypt algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- PASSWORD UTILITIES ---

def verify_password(plain_password, hashed_password):
    """Checks if the plain text password matches the hashed one in the DB."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Converts a plain text password into a secure bcrypt hash."""
    return pwd_context.hash(password)

# --- JWT UTILITIES ---

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Generates a new JWT token."""
    to_encode = data.copy()
    
    # Set the expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
        
    to_encode.update({"exp": expire})
    
    # Create the encoded JWT string
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt