import os
from dotenv import load_dotenv
load_dotenv()    

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DATABASE_TYPE = os.getenv("DATABASE_TYPE", "mysql+pymysql")
    DATABASE_HOST = os.getenv("DATABASE_HOST", "northwind-mysql-db.ccghzwgwh2c7.us-east-1.rds.amazonaws.com")
    DATABASE_PORT = os.getenv("DATABASE_PORT", 3306)
    DATABASE_USERNAME = os.getenv("DATABASE_USERNAME", "user_read_only")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "laborit_teste_2789")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "northwind")

settings = Settings()
