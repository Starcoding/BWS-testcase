from fastapi import Depends
from sqlalchemy.orm import Session

from src.db import get_db
from src.models.TransactionModel import Transaction


class TransactionRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    async def get_transaction_by_id(
        self, user_id: int, transaction_id: str
    ) -> Transaction | None:
        return (
            self.db.query(Transaction)
            .filter(
                Transaction.user_id == user_id,
                Transaction.transaction_id == transaction_id,
            )
            .first()
        )

    async def create_transaction(self, transaction: Transaction):
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction
