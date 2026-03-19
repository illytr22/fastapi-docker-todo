import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. 获取环境变量（Docker运行用），如果没有则用本地默认值
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = "root"
DB_PASSWORD = "123456"  # 👈 确保这里填对了！
DB_NAME = "todo_db"      # 👈 确保你在 MySQL 里已经手动创建了这个库！

# 2. 核心：修正连接字符串格式
# 正确格式：mysql+pymysql://用户名:密码@地址:端口/数据库名
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"

# 3. 创建引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 3. Create SessionLocal
# Each instance of SessionLocal will be a database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create the Base class
# Our database models (User, Todo) will inherit from this class.
Base = declarative_base()

# 5. Dependency: Get DB
# This function ensures the database connection is closed after the request is finished.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()