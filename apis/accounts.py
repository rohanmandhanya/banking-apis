from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from typing import List
from pydantic import parse_obj_as

from apis.users import get_customer
from db import get_db
from db.models.accounts import (
    create_new_account,
    retrieve_account,
    retrieve_account_transactions,
    # Transaction,
)
from core.transactions import start_transaction
from schemas import AccountIn, TransactionIn, UserOut, AccountOut, Transaction

router = APIRouter()


@router.post("/create", response_model=AccountOut)
def create_account(
    account: AccountIn,
    db: Session = Depends(get_db),
    customer: UserOut = Depends(get_customer),
):
    """
    This api is used to create a new account under a customer(user)
    """

    account = create_new_account(
        AccountOut(
            customer_id=customer.id,
            account_type=account.account_type,
            current_balance=account.deposit,
        ),
        db,
    )
    return AccountOut(
        customer_id=customer.id,
        account_type=account.account_type,
        current_balance=account.current_balance,
    )


@router.post("/transaction/create", response_model=AccountOut)
def initate_transaction(
    transaction: TransactionIn,
    db: Session = Depends(get_db),
    customer: UserOut = Depends(get_customer),
):
    """
    This api is used to get initate a transaction between two accounts
    """

    start_transaction(transaction, db, customer.id)

    account = retrieve_account(transaction.from_account, db, customer_id=customer.id)

    return AccountOut(
        customer_id=customer.id,
        account_type=account.account_type,
        current_balance=account.current_balance,
    )


@router.get("/balance/{account_id}", response_model=AccountOut)
def get_account_balance(
    account_id: str = Path(
        description="Account ID on which you want to check current balance"
    ),
    db: Session = Depends(get_db),
    customer: UserOut = Depends(get_customer),
):
    """
    This api is used to get account current balance
    """
    account = retrieve_account(account_id, db, customer.id)

    return AccountOut(
        customer_id=customer.id,
        account_type=account.account_type,
        current_balance=account.current_balance,
    )


@router.get("/transaction/all/{account_id}", response_model=List)
def get_account_transactions(
    account_id: str = Path(
        description="Account ID on which you want to fetch all transactions",
    ),
    db: Session = Depends(get_db),
    customer: str = Depends(get_customer),
):
    """
    This api is used to return all the transactions associated with the account
    """
    # TO authenticate user can access the account or not
    retrieve_account(account_id, db, customer.id)

    return retrieve_account_transactions(account_id, db=db)
