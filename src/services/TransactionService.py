from fastapi import Depends, HTTPException

from src.models.TransactionModel import Transaction
from src.models.UserModel import User
from src.repositories.TransactionRepository import TransactionRepository
from src.repositories.UserRepository import UserRepository
from src.schemas.TransactionSchema import BalanceUpdate


class TransactionService:
    user_repository: UserRepository
    transaction_repository: TransactionRepository

    def __init__(
        self,
        user_repository: UserRepository = Depends(),
        transaction_repository: TransactionRepository = Depends(),
    ):
        self.user_repository = user_repository
        self.transaction_repository = transaction_repository

    async def update_balance(
        self,
        user_id: int,
        balance_update: BalanceUpdate,
    ) -> User:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        if not user.is_verified:
            raise HTTPException(status_code=400, detail="Пользователь не верифицирован")

        existing_tx = await self.transaction_repository.get_transaction_by_id(
            user_id, balance_update.transaction_id
        )
        if existing_tx:
            raise HTTPException(
                status_code=400, detail="Транзакция уже была обработана"
            )

        user.balance += balance_update.amount  # type: ignore

        transaction = Transaction(
            user_id=user_id,
            transaction_id=balance_update.transaction_id,
            amount=balance_update.amount,
        )
        await self.transaction_repository.create_transaction(transaction)

        return user
