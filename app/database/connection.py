from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

load_dotenv()

username = os.getenv("DATABASE_USERNAME", "user_read_only")
password = quote_plus(os.getenv("DATABASE_PASSWORD", "laborit_teste_2789"))  # escapa caracteres especiais
host     = os.getenv("DATABASE_HOST", "northwind-mysql-db.ccghzwgwh2c7.us-east-1.rds.amazonaws.com")
port     = os.getenv("DATABASE_PORT", "3306")
name     = os.getenv("DATABASE_NAME", "northwind")

db_type  = os.getenv("DATABASE_TYPE", "mysql+pymysql")

DATABASE_URL = f"{db_type}://{username}:{password}@{host}:{port}/{name}"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,      # reconecta se a conexão cair
    pool_recycle=3600        # recicla conexões antigas
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
