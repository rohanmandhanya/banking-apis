from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship, Session
from fastapi import HTTPException, status
from datetime import datetime
import logging

from db.base_class import BaseModel
from schemas import AccountOut, TransactionIn


class Account(BaseModel):

    id = Column(Integer, primary_key=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("user.id"))
    customer = relationship("User")
    account_type = Column(String(10), unique=False, nullable=False)
    current_balance = Column(Float, unique=False, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)


class Transaction(BaseModel):

    id = Column(Integer, primary_key=True, nullable=False)
    transaction_amount = Column(Float, nullable=False)
    transaction_type = Column(String(10), unique=False, nullable=False)
    account_id = Column(Integer, ForeignKey("account.id"))
    account_id_third_party = Column(Integer, ForeignKey("account.id"))
    created_at = Column(DateTime, default=datetime.now)


def create_new_account(account: AccountOut, db: Session):

    account = Account(**account.dict())

    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def retrieve_account(id: int, db: Session, customer_id):

    account = db.query(Account).filter(Account.id == id).first()
    if account.customer_id != customer_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized User"
        )

    return account


def retrieve_account_transactions(id: int, db: Session):

    transactions = db.query(Transaction).filter(Transaction.account_id == id).all()

    return transactions


def create_new_transactions(transaction: TransactionIn, db: Session):

    try:

        transaction_to = Transaction(
            transaction_amount=transaction.amount,
            transaction_type="credit",
            account_id=transaction.to_account,
            account_id_third_party=transaction.from_account,
        )

        transaction_from = Transaction(
            transaction_amount=transaction.amount,
            transaction_type="debit",
            account_id=transaction.from_account,
            account_id_third_party=transaction.to_account,
        )

        db.add(transaction_from)
        db.add(transaction_to)

        db.commit()

        return True

    except Exception as e:
        logging.exception(e)
        return False
