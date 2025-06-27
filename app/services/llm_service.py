from openai import OpenAI
from app.config import settings

class LLMService:
    """
    Serviço responsável por gerar instruções SQL válidas para MySQL 8
    com base no banco Northwind e nas tabelas definidas.
    """
    
    _SCHEMA_CONTEXT = """
        Schema das tabelas (MySQL 8):

        Tabela: customers
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

        Tabela: employees
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

        Tabela: orders
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

        Tabela: products
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

        Tabela: order_details
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
        """

    _USE_TABLES = ["customers", "employees", "orders", "products", "order_details"]

    _BASE_SYSTEM_PROMPT = f"""
        Você é um gerador de instruções SQL para MySQL 8 usando o banco Northwind.

        Instruções:
        - Use apenas as tabelas: customers, employees, orders, products, order_details.
        - Nunca use colchetes ([ ]) ou espaços nos nomes de tabelas ou colunas.
        - Retorne **apenas** o código SQL dentro de um bloco markdown ```sql ... ```.
        - Logo após o bloco SQL, forneça uma breve explicação textual simples da consulta no formato:
        Explicação: <texto explicativo>
        - A query deve ser uma instrução SELECT válida.
        - Não inclua nada além do bloco SQL e a explicação.

        {_SCHEMA_CONTEXT}
        """

    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def answer_question(self, question: str) -> str:
        """
        Gera uma query SQL com base em uma pergunta simples, usando o prompt base.
        """
        messages = [
            {"role": "system", "content": self._BASE_SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ]

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.1,
        )
        return response.choices[0].message.content.strip()

    def generate_sql(self, question: str, context: str = "") -> str:
        """
        Gera uma query SQL com contexto extra (como schema ou exemplos).
        """
        messages = [
            {"role": "system", "content": self._BASE_SYSTEM_PROMPT},
            {"role": "user", "content": f"{question}\n\nContexto adicional:\n{context}"}
        ]

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.1,
        )
        return response.choices[0].message.content.strip()
