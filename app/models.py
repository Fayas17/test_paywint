import sqlalchemy
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base

class Expense(Base):
    __tablename__ = "expense"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()  # Annotated correctly
    amount: Mapped[float] = mapped_column()
    category: Mapped[str] = mapped_column()
