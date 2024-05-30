from schemas import TransactionIn
from core.transactions import start_transaction
from db.models.accounts import retrieve_account_transactions, retrieve_account
from utils import create_test_user, create_test_accounts


def test_start_transaction(client, db_session):

    user = create_test_user(db_session)
    a1, a2 = create_test_accounts(user.id, db_session)

    test_transaction = TransactionIn(
        **{"to_account": a2.id, "from_account": a1.id, "amount": 100}
    )

    start_transaction(test_transaction, db_session, user.id)

    a2_transactions = retrieve_account_transactions(a2.id, db_session)
    a1_transactions = retrieve_account_transactions(a2.id, db_session)

    a1 = retrieve_account(a1.id, db_session, user.id)
    a2 = retrieve_account(a2.id, db_session, user.id)

    assert len(a1_transactions) == 1
    assert len(a2_transactions) == 1

    assert a1.current_balance == 999900
    assert a2.current_balance == 1100
