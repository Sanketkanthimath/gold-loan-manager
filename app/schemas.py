from pydantic import BaseModel
from datetime import date
from typing import Optional

class CustomerBase(BaseModel):
    name: str
    gold_weight: float
    loan_amount: float
    loan_date: date

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    photo_path: Optional[str] = None

    class Config:
        orm_mode = True