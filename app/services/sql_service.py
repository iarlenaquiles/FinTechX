import re
from app.services.llm_service import LLMService
from app.repositories.db_repository import DBRepository

ALLOWED_TABLES = {"customers", "employees", "orders", "products", "order_details"}

class SQLService:
    def __init__(self, llm_service: LLMService, db: DBRepository):
        self.llm = llm_service
        self.db = db

    def _validate_sql_tables(self, sql: str):
        found_tables = re.findall(r"\b(from|join)\s+`?([a-zA-Z_]+)`?", sql, re.IGNORECASE)
        for _, table in found_tables:
            if table.lower() not in ALLOWED_TABLES:
                raise ValueError(f"Tabela não permitida: '{table}'")

    def process_question(self, question: str):
        response = self.llm.generate_sql_with_context(question)

        sql_match = re.search(r"```sql\s+(.*?)```", response, re.DOTALL | re.IGNORECASE)
        if not sql_match:
            raise ValueError("SQL não encontrado na resposta do LLM")
        sql = sql_match.group(1).strip()

        explanation_match = re.search(r"Explicação:\s*(.*)", response, re.DOTALL | re.IGNORECASE)
        explanation = explanation_match.group(1).strip() if explanation_match else "Sem explicação fornecida."

        self._validate_sql_tables(sql)

        data = self.db.run_query(sql)

        return {
            "sql": re.sub(r"\s+", " ", sql).strip(),
            "data": data,
            "explanation": explanation,
        }