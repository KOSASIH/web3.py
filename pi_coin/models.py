from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel, EmailStr, constr

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to transactions
    sent_transactions = relationship("Transaction", foreign_keys='Transaction.sender_id', back_populates="sender")
    received_transactions = relationship("Transaction", foreign_keys='Transaction.receiver_id', back_populates="receiver")

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_transactions")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_transactions")

# Pydantic models for data validation
class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=30)
    full_name: str
    email: EmailStr
    password: constr(min_length=8)

class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    email: EmailStr
    disabled: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class TransactionCreate(BaseModel):
    sender_id: int
    receiver_id: int
    amount: float

class TransactionResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    amount: float
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
