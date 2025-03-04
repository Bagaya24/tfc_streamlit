from typing import List
from pydantic import BaseModel, Field
from datetime import datetime

class QueryInput(BaseModel):
    question: str
    session_id: str = Field(None)

class QueryResponse(BaseModel):
    answer: str
    session_id: str

class DetailAchat(BaseModel):
    product_names : List[str] | None
    product_prices : List[float] | None


