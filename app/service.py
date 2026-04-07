from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from typing import List

from .db import get_db
from .models import Expense


router = APIRouter()


class ExpenseCreate(BaseModel):
    """Schema for creating a new expense."""
    name: str
    amount: float
    category: str


class ExpenseResponse(BaseModel):
    """Schema for returning expense details."""
    expense_id: int
    name: str
    amount: float
    category: str

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm_expense(cls, expense: Expense) -> "ExpenseResponse":
        return cls(
            expense_id=expense.id,
            name=expense.name,
            amount=expense.amount,
            category=expense.category,
        )


@router.post("/expenses/", response_model=ExpenseResponse, status_code=201)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    """Create a new expense record."""
    db_expense = Expense(
        name=expense.name,
        amount=expense.amount,
        category=expense.category,
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return ExpenseResponse.from_orm_expense(db_expense)


@router.get("/expenses/", response_model=List[ExpenseResponse])
def get_expenses(db: Session = Depends(get_db)):
    """Retrieve a list of all expenses."""
    expenses = db.query(Expense).all()
    return [ExpenseResponse.from_orm_expense(e) for e in expenses]
