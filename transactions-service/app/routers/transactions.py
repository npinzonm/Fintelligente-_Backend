from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies import get_current_user
from ..database import get_db
from .. import models, schemas
from ..ai_service import categorize_transaction

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/", response_model=schemas.TransactionOut)
def create_transaction(
    data: schemas.TransactionCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # Si no viene categoría → la IA lo clasifica
    if not data.category:
        data.category = categorize_transaction(
            description=data.description,
            amount=data.amount
        )

    tx = models.Transaction(
        **data.dict(),
        user_id=current_user["id"]
    )

    db.add(tx)
    db.commit()
    db.refresh(tx)

    return tx

@router.post("/batch", response_model=List[schemas.TransactionOut])
def batch_create_transactions(
    data: List[schemas.TransactionCreate],
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    items = [{"description": t.description, "amount": t.amount} for t in data]
    categories = batch_categorize(items)

    results = []
    for i, t in enumerate(data):
        tx = models.Transaction(
            description=t.description,
            amount=t.amount,
            date=t.date,
            category=categories[i],
            user_id=current_user["id"]
        )
        db.add(tx)
        db.commit()
        db.refresh(tx)
        results.append(tx)

    return results