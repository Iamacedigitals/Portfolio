import uuid
from typing import List, Optional
from datetime import datetime

from sqlalchemy import Column, func, String, DateTime, ForeignKey, BigInteger, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlmodel import SQLModel, Field

class CryptoResonse(SQLModel, table = True):
    __tablename__ = "Crypto_Response"

    crypto_pair: str = Field(
        sa_column = Column(String(50), nullable=False, primary_key=True)
        )
    
    Open_time: int = Field(
        sa_column = Column(BigInteger, nullable=False, primary_key=True)
        )
    
    Close_time: int = Field(
        sa_column = Column(BigInteger, nullable=False)
        )
    
    open_: float  = Field(
        sa_column = Column(Float, nullable=False)
        )
    
    high: float = Field(
        sa_column = Column(Float, nullable=False)
        )
    
    low: float = Field(
        sa_column = Column(Float, nullable=False)
        )
    
    close: float = Field(
        sa_column = Column(Float, nullable=False)
        )
    
    Volume: str = Field(
        sa_column = Column(String, nullable=False)
        )
    
    Volume_Quote: str = Field(
        sa_column = Column(String, nullable=False)
        )
    
    def __repr__(self):
        return f"<User {self.crypto_pair}>"