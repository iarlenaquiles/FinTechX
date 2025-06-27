from fastapi import APIRouter, Depends
from app.schemas.query_schema import QueryRequest, QueryResponse
from app.services.llm_service import LLMService
from app.repositories.db_repository import DBRepository
from app.services.sql_service import SQLService
from sqlalchemy.orm import Session
from app.database.connection import get_db
from sqlalchemy import text

router = APIRouter()

def get_sql_service(db: Session = Depends(get_db)):
    return SQLService(LLMService(), DBRepository(db))

@router.post("/query")
def query_data(request: QueryRequest, service: SQLService = Depends(get_sql_service)):
    result = service.process_question(request.question)
    return QueryResponse(**result)

@router.get("/ping-db")
def ping_db(db: Session = Depends(get_db)):
    result = db.execute(text("SHOW COLUMNS FROM employees;")).scalar()
    print(result)
    return result