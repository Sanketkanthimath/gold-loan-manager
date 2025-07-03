from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    gold_weight = Column(Float, nullable=False)
    loan_amount = Column(Float, nullable=False)
    loan_date = Column(Date, nullable=False)
    photo_path = Column(String, nullable=True)