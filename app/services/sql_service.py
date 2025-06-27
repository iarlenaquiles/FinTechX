import re
from app.services.llm_service import LLMService
from app.repositories.db_repository import DBRepository
import hashlib
from fastapi_cache.decorator import cache
import json
from decimal import Decimal

ALLOWED_TABLES = {"customers", "employees", "orders", "products", "order_details"}

class SQLService:
    def __init__(self, llm_service: LLMService, db: DBRepository,  redis_client):
        self.llm = llm_service
        self.db = db
        self.redis = redis_client

    def _validate_sql_tables(self, sql: str):
        found_tables = re.findall(r"\b(from|join)\s+`?([a-zA-Z_]+)`?", sql, re.IGNORECASE)
        for _, table in found_tables:
            if table.lower() not in ALLOWED_TABLES:
                raise ValueError(f"Tabela não permitida: '{table}'")

    def _hash(self, value: str) -> str:
        return hashlib.sha256(value.encode()).hexdigest()
    
    async def process_question(self, question: str):
        return await self._cached_process(question)
    
    def _hash(self, value: str) -> str:
        return hashlib.sha256(value.encode()).hexdigest()
    
    @cache(expire=60 * 5)
    async def _cached_process(self, question: str):
        # Verifica cache da pergunta
        question_key = f"question:{self._hash(question)}"
        cached = self.redis.get(question_key)
        if cached:
            return json.loads(cached)
        
        response = self.llm.generate_sql_with_context(question)

        sql_match = re.search(r"```sql\s+(.*?)```", response, re.DOTALL | re.IGNORECASE)
        if not sql_match:
            raise ValueError("SQL não encontrado na resposta do LLM")
        sql = sql_match.group(1).strip()

        explanation_match = re.search(r"Explicação:\s*(.*)", response, re.DOTALL | re.IGNORECASE)
        explanation = explanation_match.group(1).strip() if explanation_match else "Sem explicação fornecida."

        self._validate_sql_tables(sql)

        rows = self.db.run_query(sql)

        data = [dict(r) for r in rows]
        response_data =  {
            "sql": re.sub(r"\s+", " ", sql).strip(),
            "data": data,
            "explanation": explanation,
        }

        self.redis.setex(question_key, 600, json.dumps(response_data, default=str))  # 10 minutos
        return response_data