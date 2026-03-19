from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from . import auth  # Import our new auth module
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

# Import our local modules
from . import models, schemas, crud, database
from .database import engine, get_db

# This line tells SQLAlchemy to create the tables in MySQL 
# if they don't exist yet.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="My Pro Backend System")

# This tells FastAPI where the client can get the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the token using our secret key
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    # Check if the user actually still exists in the database
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI system! Check /docs for Swagger UI"}

# Example Route: Create a User (Basic version without Hashing for now)
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 1. Ask CRUD if the email exists
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 2. Ask CRUD to create the user
    return crud.create_user(db=db, user=user)

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # ==== 🕵️ 开始打印调试信息 ====
    print("\n" + "="*40)
    print("🕵️ DEBUG LOGIN FLOW STARTED")
    print(f"1. 前端传来的账号: '{form_data.username}'")
    print(f"2. 前端传来的密码: '{form_data.password}'")
    
    # 1. Fetch the user from the database
    user = crud.get_user_by_email(db, email=form_data.username)
    
    if not user:
        print("3. 查询结果: ❌ 失败！数据库里根本没有这个邮箱！")
        print("="*40 + "\n")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    print(f"3. 查询结果: ✅ 成功！找到了用户 (ID: {user.id})")
    print(f"   数据库里存的密码 Hash 是: '{user.hashed_password}'")
    
    # 2. Verify user exists AND password is correct
    is_password_correct = auth.verify_password(form_data.password, user.hashed_password)
    print(f"4. 密码校验结果: {is_password_correct}")
    print("="*40 + "\n")
    # ==== 🕵️ 调试信息打印结束 ====

    if not is_password_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Generate the JWT Access Token
    access_token = auth.create_access_token(data={"sub": user.email})
    
    # 4. Return the exact JSON structure required by OAuth2
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/todos/", response_model=schemas.Todo)
def create_todo_for_user(
    todo: schemas.TodoCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # THE BOUNCER!
):
    # Notice we don't need the user to send their user_id. 
    # We securely extract it from the JWT token via 'current_user'
    return crud.create_user_todo(db=db, todo=todo, user_id=current_user.id)

