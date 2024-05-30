import json
from core.security import create_access_token
from utils import create_test_user, create_test_accounts


def test_create_user(client):

    test_user = {
        "first_name": "rohan",
        "last_name": "m",
        "age": 28,
        "gender": "male",
        "phone_number": "123-124-0052",
        "email": "rohan1@test.co",
        "address_line_one": "123",
        "address_line_two": "st",
        "city": "SF",
        "state": "CA",
        "country": "USA",
        "pincode": "12345",
        "birthdate": "1994-04-29",
        "password": "fake",
    }

    response = client.post(
        "/user/create",
        headers={"Content-type": "application/json"},
        data=json.dumps(test_user),
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == test_user["first_name"]
    assert data["last_name"] == test_user["last_name"]


def test_create_account(client, db_session):
    test_account = {"account_type": "saving", "deposit": 10000}
    headers = {}

    user = create_test_user(db=db_session)

    token_data = create_access_token(user.customer_id)
    headers["Authorization"] = "Bearer " + token_data
    headers["Content-type"] = "application/json"
    response = client.post(
        "/account/create",
        headers=headers,
        data=json.dumps(test_account),
    )
    data = response.json()

    assert response.status_code == 200
    assert data["account_type"] == test_account["account_type"]
    assert data["current_balance"] == test_account["deposit"]


def test_unauthorized_user(client, db_session):
    test_account = {"account_type": "saving", "deposit": 10000}
    headers = {}

    headers["Content-type"] = "application/json"
    response = client.post(
        "/account/create",
        headers=headers,
        data=json.dumps(test_account),
    )
    data = response.json()
    print(data)

    assert response.status_code == 401
    assert data["detail"] == "Not authenticated"


def test_initate_transaction(client, db_session):
    headers = {}

    user = create_test_user(db=db_session)

    token_data = create_access_token(user.customer_id)

    a1, a2 = create_test_accounts(user.id, db=db_session)

    headers["Authorization"] = "Bearer " + token_data
    headers["Content-type"] = "application/json"

    test_transaction = {"to_account": a2.id, "from_account": a1.id, "amount": 100}

    response = client.post(
        "/account/transaction/create",
        headers=headers,
        data=json.dumps(test_transaction),
    )

    data = response.json()

    assert response.status_code == 200
    assert data["account_type"] == a1.account_type
    assert data["current_balance"] == 999900


def test_initate_transaction_account_not_found(client, db_session):
    headers = {}

    user = create_test_user(db=db_session)

    token_data = create_access_token(user.customer_id)

    a1, a2 = create_test_accounts(user.id, db=db_session)

    headers["Authorization"] = "Bearer " + token_data
    headers["Content-type"] = "application/json"

    test_transaction = {"to_account": a2.id, "from_account": "100000000", "amount": 100}

    response = client.post(
        "/account/transaction/create",
        headers=headers,
        data=json.dumps(test_transaction),
    )

    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "No Account under that user"


def test_initate_transaction_third_account_not_found(client, db_session):
    headers = {}

    user = create_test_user(db=db_session)

    token_data = create_access_token(user.customer_id)

    a1, a2 = create_test_accounts(user.id, db=db_session)

    headers["Authorization"] = "Bearer " + token_data
    headers["Content-type"] = "application/json"

    test_transaction = {"to_account": "11111111", "from_account": a1.id, "amount": 100}

    response = client.post(
        "/account/transaction/create",
        headers=headers,
        data=json.dumps(test_transaction),
    )

    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "Account Not found"


def test_initate_transaction_low_balance(client, db_session):
    headers = {}

    user = create_test_user(db=db_session)

    token_data = create_access_token(user.customer_id)

    a1, a2 = create_test_accounts(user.id, db=db_session)

    headers["Authorization"] = "Bearer " + token_data
    headers["Content-type"] = "application/json"

    test_transaction = {"to_account": a1.id, "from_account": a2.id, "amount": 1111}

    response = client.post(
        "/account/transaction/create",
        headers=headers,
        data=json.dumps(test_transaction),
    )

    data = response.json()

    assert response.status_code == 400
    assert data["detail"] == "Balance low for the transaction"


def test_get_current_balance(client, db_session):

    user = create_test_user(db=db_session)
    headers = {}

    token_data = create_access_token(user.customer_id)

    headers["Authorization"] = "Bearer " + token_data
    headers["Content-type"] = "application/json"

    a1, a2 = create_test_accounts(user.id, db=db_session)

    response = client.get(f"/account/balance/{a1.id}", headers=headers)

    data = response.json()

    assert response.status_code == 200
    assert data["account_type"] == a1.account_type
    assert data["current_balance"] == 1000000


def test_get_current_balance_unauthorized(client, db_session):

    user = create_test_user(db=db_session)
    headers = {}

    token_data = create_access_token("12345")

    headers["Authorization"] = "Bearer " + token_data
    headers["Content-type"] = "application/json"

    a1, a2 = create_test_accounts(user.id, db=db_session)

    response = client.get(f"/account/balance/{a1.id}", headers=headers)

    data = response.json()

    assert response.status_code == 401
    assert data["detail"] == "Unauthorized User"


def test_get_account_transactions(client, db_session):

    user = create_test_user(db=db_session)
    headers = {}

    token_data = create_access_token(user.customer_id)

    headers["Authorization"] = "Bearer " + token_data
    headers["Content-type"] = "application/json"

    a1, a2 = create_test_accounts(user.id, db=db_session)

    response = client.get(f"/account/transaction/all/{a2.id}", headers=headers)
    assert response.status_code == 200
    assert response.json() == []


def test_get_account_transactions_unauthorized(client, db_session):

    user = create_test_user(db=db_session)
    headers = {}

    token_data = create_access_token("12345")

    headers["Authorization"] = "Bearer " + token_data
    headers["Content-type"] = "application/json"

    a1, a2 = create_test_accounts(user.id, db=db_session)

    response = client.get(f"/account/transaction/all/{a2.id}", headers=headers)

    data = response.json()

    assert response.status_code == 401
    assert data["detail"] == "Unauthorized User"
