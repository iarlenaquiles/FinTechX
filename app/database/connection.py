from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

username = settings.DATABASE_USERNAME
password = settings.DATABASE_PASSWORD
host     = settings.DATABASE_HOST
port     = settings.DATABASE_PORT
name     = settings.DATABASE_NAME

db_type  = settings.DATABASE_TYPE

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
