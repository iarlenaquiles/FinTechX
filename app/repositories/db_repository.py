from sqlalchemy.orm import Session
from sqlalchemy import text

class DBRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def run_query(self, query: str) -> list[dict]:
        """
        Executa a query e devolve uma lista de dicionários (coluna → valor).
        Usa `.mappings()` para garantir que cada linha venha como RowMapping.
        """
        result = self.db.execute(text(query))
        return result.mappings().all()        # ← solução correta
        # se preferir compatibilidade ampla:
        # return [dict(row._mapping) for row in result]