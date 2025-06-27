import re
from app.services.llm_service import LLMService
from app.repositories.db_repository import DBRepository
import hashlib
import json
import redis

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
    
    def process_question(self, question: str):
        # Verifica cache da pergunta
        question_key = f"question:{self._hash(question)}"
        cached = self.redis.get(question_key)
        if cached:
            return json.loads(cached)

        # Gera resposta do LLM
        response = self.llm.answer_question(question)

        # Extrai SQL
        match = re.search(r"```sql\s+(.*?)```", response, re.DOTALL | re.IGNORECASE)
        if not match:
            raise ValueError("SQL não encontrado na resposta do LLM")
        sql = match.group(1).strip()

        # Valida SQL
        self._validate_sql_tables(sql)

        # Executa e armazena resultado da query
        result = self._run_query_with_cache(sql)

        # Monta a resposta final
        response_data = {
            "sql": re.sub(r"\s+", " ", sql).strip(),
            "data": result,
            "explanation": f"Consulta gerada para responder: “{question}”"
        }

        # Armazena no cache
        self.redis.setex(question_key, 600, json.dumps(response_data))  # 10 minutos
        return response_data
    
    def _run_query_with_cache(self, sql: str):
        sql_key = f"sql:{self._hash(sql)}"
        cached = self.redis.get(sql_key)
        if cached:
            return json.loads(cached)

        data = self.db.run_query(sql)
        self.redis.setex(sql_key, 600, json.dumps(data))
        return data