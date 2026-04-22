# 🚀 FinTechX LLM-SQL API

An intelligent API that transforms **natural language questions** into **optimized SQL queries** over the **Northwind (MySQL)** database, using language models (LLMs), semantic validation, and RAG (retrieval-augmented generation).

---

## 📌 Table of Contents

- [✨ Overview](#-overview)
- [🧠 Technologies Used](#-technologies-used)
- [🧱 Architecture](#-architecture)
- [🚀 How to Run Locally](#-how-to-run-locally)
- [🔐 Environment Variables](#-environment-variables)
- [📡 API Endpoints](#-api-endpoints)
- [📊 Usage Examples](#-usage-examples)
- [🧪 Tests](#-tests)
- [☁️ Cloud Deployment (CI/CD)](#-cloud-deployment-cicd)
- [📎 References](#-references)

---

## ✨ Overview

FinTechX faces challenges such as:

- Low personalization in customer service  
- Complex processes  
- Limited predictive and analytical capabilities  

### 🎯 Proposed Solution

An **LLM-powered API** that:

- Interprets human questions  
- Generates secure and explainable SQL  
- Returns data and insights with high performance  

---

## 🧠 Technologies Used

| Category | Technology |
|---|---|
| Backend API | FastAPI |
| Database | MySQL (Northwind) |
| LLM | OpenAI GPT-4 |
| Vector Search (RAG) | FAISS (optional) |
| Cache | Redis (optional) |
| SQL Validation | `sqlglot`, `sqlvalidator` |
| Frontend (optional) | Streamlit |
| Testing | Pytest / Postman |
| CI/CD | GitHub Actions / Render |

---

## 🧱 Architecture

```text
User → FastAPI → GPT-4 → SQL Generation → SQL Validation → MySQL (Northwind)
                     ↑                 ↓
                 RAG / Cache     Data + Explanation
```

- Modular architecture (following SOLID principles)
- Clear separation of responsibilities (services, repositories, schemas)
- Extensible for metrics, security, and visual frontend

---

## 🚀 How to Run Locally

### 1. Clone the project

```bash
git clone https://github.com/iarlenaquiles/fintechx.git
cd fintechx
```

### 2. Create the virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root or copy from `.env.example`:

```env
OPENAI_API_KEY=sk-...
DATABASE_HOST=northwind-mysql-db.ccghzwgwh2c7.us-east-1.rds.amazonaws.com
DATABASE_USERNAME=user_read_only
DATABASE_PASSWORD=laborit_teste_2789
DATABASE_NAME=northwind
```

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

Access Swagger documentation at:

📍 http://localhost:8000/docs

---

## 🔐 Environment Variables

| Name | Description |
|---|---|
| OPENAI_API_KEY | OpenAI API key |
| DATABASE_HOST | MySQL database host |
| DATABASE_USERNAME | Read-only database user |
| DATABASE_PASSWORD | Database password |
| DATABASE_NAME | Database name (`northwind`) |

---

## 📡 API Endpoints

### POST `/query`

Query the database using natural language.

### Request Body

```json
{
  "question": "What are the best-selling products?"
}
```

### Response

```json
{
  "sql": "...",
  "data": [...],
  "explanation": "Query created to retrieve the best-selling products by quantity."
}
```

---

## 📊 Usage Examples

### Supported Questions

```text
Which products are the most popular among corporate customers?

What is the sales volume by city?

Which customers made the most purchases?

What is the average ticket per purchase?
```

---

## 🧪 Tests

### Run tests

```bash
pytest tests/
```

Or import the Postman collection located at:

`tests/FinTechX.postman_collection.json`

---

## ☁️ Cloud Deployment (CI/CD)

- Dockerfile included (optional)
- Deploy on Render or Railway
- `render.yaml` for automatic CI/CD
- GitHub Actions (`.github/workflows/deploy.yml`)

---

## 📎 References

- FastAPI Documentation
- Northwind Database Schema
- OpenAI API
- LangChain
- RAG Pattern

---

## 🐳 Steps to Run the Application with Docker

### 1. Clone the repository (if you haven’t already)

```bash
git clone <REPOSITORY_URL>
cd <REPOSITORY_NAME>
```

### 2. Build and start the containers using Docker Compose

```bash
docker compose up --build
```

### 3. The FastAPI application will be available at:

```text
http://localhost:8000
```

### 4. To stop the containers, use:

```bash
docker compose down
```

