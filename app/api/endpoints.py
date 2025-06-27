from fastapi import APIRouter, Depends
from app.schemas.query_schema import QueryRequest, QueryResponse
from app.services.llm_service import LLMService
from app.repositories.db_repository import DBRepository
from app.services.sql_service import SQLService
from sqlalchemy.orm import Session
from app.database.connection import get_db
from sqlalchemy import text
from app.services.retriever_service import RetrieverService
from redis import Redis

router = APIRouter()

documents = [
    """
    Schema da tabela customers:
    - id INT PRIMARY KEY AUTO_INCREMENT
    - company VARCHAR(50)
    - last_name VARCHAR(50)
    - first_name VARCHAR(50)
    - email_address VARCHAR(50)
    - job_title VARCHAR(50)
    - business_phone VARCHAR(25)
    - home_phone VARCHAR(25)
    - mobile_phone VARCHAR(25)
    - fax_number VARCHAR(25)
    - address LONGTEXT
    - city VARCHAR(50)
    - state_province VARCHAR(50)
    - zip_postal_code VARCHAR(15)
    - country_region VARCHAR(50)
    - web_page LONGTEXT
    - notes LONGTEXT
    - attachments LONGBLOB
    """,

    """
    Schema da tabela employees:
    - id INT PRIMARY KEY AUTO_INCREMENT
    - company VARCHAR(50)
    - last_name VARCHAR(50)
    - first_name VARCHAR(50)
    - email_address VARCHAR(50)
    - job_title VARCHAR(50)
    - business_phone VARCHAR(25)
    - home_phone VARCHAR(25)
    - mobile_phone VARCHAR(25)
    - fax_number VARCHAR(25)
    - address LONGTEXT
    - city VARCHAR(50)
    - state_province VARCHAR(50)
    - zip_postal_code VARCHAR(15)
    - country_region VARCHAR(50)
    - web_page LONGTEXT
    - notes LONGTEXT
    - attachments LONGBLOB
    """,

    """
    Schema da tabela orders:
    - id INT PRIMARY KEY AUTO_INCREMENT
    - employee_id INT
    - customer_id INT
    - order_date DATETIME
    - shipped_date DATETIME
    - shipper_id INT
    - ship_name VARCHAR(50)
    - ship_address LONGTEXT
    - ship_city VARCHAR(50)
    - ship_state_province VARCHAR(50)
    - ship_zip_postal_code VARCHAR(50)
    - ship_country_region VARCHAR(50)
    - shipping_fee DECIMAL(19,4) DEFAULT 0.0000
    - taxes DECIMAL(19,4) DEFAULT 0.0000
    - payment_type VARCHAR(50)
    - paid_date DATETIME
    - notes LONGTEXT
    - tax_rate DOUBLE DEFAULT 0
    - tax_status_id TINYINT
    - status_id TINYINT DEFAULT 0
    """,

    """
    Schema da tabela products:
    - id INT PRIMARY KEY AUTO_INCREMENT
    - supplier_ids LONGTEXT
    - product_code VARCHAR(25)
    - product_name VARCHAR(50)
    - description LONGTEXT
    - standard_cost DECIMAL(19,4) DEFAULT 0.0000
    - list_price DECIMAL(19,4) NOT NULL DEFAULT 0.0000
    - reorder_level INT
    - target_level INT
    - quantity_per_unit VARCHAR(50)
    - discontinued TINYINT(1) NOT NULL DEFAULT 0
    - minimum_reorder_quantity INT
    - category VARCHAR(50)
    - attachments LONGBLOB
    """,

    """
    Schema da tabela order_details:
    - id INT PRIMARY KEY AUTO_INCREMENT
    - order_id INT NOT NULL
    - product_id INT
    - quantity DECIMAL(18,4) NOT NULL DEFAULT 0.0000
    - unit_price DECIMAL(19,4) DEFAULT 0.0000
    - discount DOUBLE NOT NULL DEFAULT 0
    - status_id INT
    - date_allocated DATETIME
    - purchase_order_id INT
    - inventory_id INT
    """,

    """
    Exemplo de consulta:
    Para listar clientes do Brasil:
    SELECT first_name, last_name FROM customers WHERE country_region = 'Brazil';
    """
]

retriever = RetrieverService(documents)
redis_client = Redis(host='localhost', port=6379, db=0)

def get_sql_service(db: Session = Depends(get_db)):
    return SQLService(LLMService(retriever), DBRepository(db), redis_client)

@router.post("/query")
def query_data(request: QueryRequest, service: SQLService = Depends(get_sql_service)):
    result = service.process_question(request.question)
    return QueryResponse(**result)

@router.get("/ping-db")
def ping_db(db: Session = Depends(get_db)):
    result = db.execute(text("SHOW COLUMNS FROM employees;")).scalar()
    print(result)
    return result