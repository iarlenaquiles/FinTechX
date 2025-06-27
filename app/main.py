from fastapi import FastAPI
from app.api import endpoints

app = FastAPI(title="FinTechX API")

app.include_router(endpoints.router)