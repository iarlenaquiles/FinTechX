from pydantic import BaseModel
from typing import List, Optional, Dict

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    sql: str
    data: List[Dict]
    explanation: Optional[str] = None 