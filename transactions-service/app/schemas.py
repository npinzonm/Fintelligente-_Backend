from pydantic import BaseModel
from datetime import date
from typing import Optional

class TransactionBase(BaseModel):
    date: date
    description: str
    amount: float
    category: Optional[str] = None
    source: Optional[str] = "MANUAL"

class TransactionCreate(TransactionBase):
    pass

class TransactionOut(TransactionBase):
    id: int

    class Config:
        from_attributes = True