# 🚀 FinTechX LLM-SQL API

API inteligente que transforma **perguntas em linguagem natural** em **consultas SQL otimizadas** sobre o banco de dados **Northwind (MySQL)**, utilizando modelos de linguagem (LLMs), validação semântica e RAG (retrieval-augmented generation).

---

## 📌 Índice

- [✨ Visão Geral](#-visão-geral)
- [🧠 Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [🧱 Arquitetura](#-arquitetura)
- [🚀 Como Executar Localmente](#-como-executar-localmente)
- [🔐 Variáveis de Ambiente](#-variáveis-de-ambiente)
- [📡 Endpoints da API](#-endpoints-da-api)
- [📊 Exemplos de Uso](#-exemplos-de-uso)
- [🧪 Testes](#-testes)
- [☁️ Deploy em Nuvem (CI/CD)](#-deploy-em-nuvem-cicd)
- [📎 Referências](#-referências)

---

## ✨ Visão Geral

A FinTechX enfrenta desafios como:

- Atendimento pouco personalizado  
- Processos complexos  
- Baixa capacidade preditiva e analítica  

### 🎯 Solução proposta:
Uma **API LLM-powered** que:

- Interpreta perguntas humanas  
- Gera SQL seguro e explicável  
- Retorna dados e insights com alta performance  

---

## 🧠 Tecnologias Utilizadas

| Categoria        | Tecnologia               |
|------------------|---------------------------|
| Backend API      | FastAPI                  |
| Banco de Dados   | MySQL (Northwind)        |
| LLM              | OpenAI GPT-4             |
| Vetorização (RAG)| FAISS (opcional)         |
| Cache            | Redis (opcional)         |
| Validação SQL    | `sqlglot`, `sqlvalidator`|
| Front (opcional) | Streamlit                |
| Testes           | Pytest / Postman         |
| CI/CD            | GitHub Actions / Render  |

---

## 🧱 Arquitetura

```text
Usuário → FastAPI → GPT-4 → Geração SQL → Validação SQL → MySQL (Northwind)
                          ↑              ↓
                      RAG / Cache   Dados + Explicação
```

- Modular (seguindo SOLID)

- Separação clara de responsabilidades (services, repositories, schemas)

- Extensível para métricas, segurança e frontend visual

## 🚀 Como Executar Localmente
1. Clone o projeto

```
git clone https://github.com/iarlenaquiles/fintechx.git
cd fintechx
```

2. Crie o ambiente virtual

```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
````

3. Instale as dependências

```
pip install -r requirements.txt
```

4. Configure variáveis de ambiente
Crie um arquivo .env na raiz com ou copie do .env.example:

.env
```
OPENAI_API_KEY=sk-...
DATABASE_HOST=northwind-mysql-db.ccghzwgwh2c7.us-east-1.rds.amazonaws.com
DATABASE_USERNAME=user_read_only
DATABASE_PASSWORD=laborit_teste_2789
DATABASE_NAME=northwind
```

5. Execute o servidor

```
uvicorn app.main:app --reload
```

Acesse a documentação Swagger em:

📍 http://localhost:8000/docs

## 🔐 Variáveis de Ambiente

|Nome	|Descrição                    |
|--------------|-----------------------|
OPENAI_API_KEY	Chave da API da OpenAI
DATABASE_HOST	Host do banco MySQL
DATABASE_USERNAME	Usuário de leitura do banco
DATABASE_PASSWORD	Senha do banco
DATABASE_NAME	Nome do banco (northwind)

## 📡 Endpoints da API

POST /query
Consulta o banco de dados com linguagem natural.

Body:
```
{
  "question": "Quais são os produtos mais vendidos?"
}
```
Response:
```
{
  "sql": "...",
  "data": [...],
  "explanation": "Consulta criada para buscar os produtos mais vendidos em quantidade."
}
```

## 📊 Exemplos de Uso
Perguntas suportadas:
```
Quais são os produtos mais populares entre os clientes corporativos?

Qual o volume de vendas por cidade?

Quais são os clientes que mais compraram?

Qual é o ticket médio por compra?
```

🧪 Testes
Rodar os testes
```
pytest tests/
```
Ou importar a coleção no Postman (em tests/FinTechX.postman_collection.json).

## ☁️ Deploy em Nuvem (CI/CD)
Dockerfile incluso (opcional)

Deploy em Render ou Railway:

render.yaml para CI/CD automático

GitHub Actions (.github/workflows/deploy.yml)

## 📎 Referências
FastAPI Documentation

Northwind Database Schema

OpenAI API

LangChain

RAG Pattern

## Passos para rodar a aplicação com Docker

1. Clone o repositório (se ainda não tiver):

```
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>
```

2. Construa e suba os containers com Docker Compose:
```
docker compose up --build
```
3. A aplicação FastAPI estará rodando em:
```
http://localhost:8000
```

4. Para parar os containers, use:
```
docker compose down
```