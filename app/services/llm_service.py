from openai import OpenAI
from app.config import settings
from app.interface.IRetriever import IRetriever

class LLMService:
    """
    Serviço responsável por gerar instruções SQL válidas para MySQL 8
    com base no banco Northwind e nas tabelas definidas.
    """

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
        """

    def __init__(self, retriever: IRetriever) -> None:
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.retriever = retriever

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

    def generate_sql_with_context(self, question: str) -> str:
        context = self.retriever.retrieve(question)
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
