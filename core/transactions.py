from datetime import datetime
from fastapi import HTTPException, status

from db.models.accounts import Account, create_new_transactions
from schemas.accounts import TransactionIn


def start_transaction(transaction: TransactionIn, db, customer_id):

    account = db.query(Account).filter(Account.id == transaction.from_account).first()
    to_account = db.query(Account).filter(Account.id == transaction.to_account).first()

    if not account:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No Account under that user",
        )

    if account.customer_id != customer_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized User"
        )

    if not to_account:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account Not found",
        )

    if transaction.amount > account.current_balance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Balance low for the transaction",
        )

    account.current_balance = account.current_balance - transaction.amount
    account.updated_at = datetime.now()

    to_account.current_balance = to_account.current_balance + transaction.amount
    to_account.updated_at = datetime.now()

    db.add(account)
    db.add(to_account)

    if create_new_transactions(transaction, db):
        db.commit()

    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong. Please contact support",
        )
