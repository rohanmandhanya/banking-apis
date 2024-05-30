from db.models.users import create_new_user
from db.models.accounts import create_new_account
from schemas import UserIn, AccountOut
from sqlalchemy.orm import Session


def create_test_user(db: Session):
    user = UserIn(
        first_name="rohan",
        last_name="m",
        age=28,
        gender="male",
        phone_number="123-124-0052",
        email="rohan@test.co",
        address_line_one="123",
        address_line_two="st",
        city="SF",
        state="CA",
        country="USA",
        pincode="12345",
        birthdate="1994-04-29",
        password="fake",
    )
    user = create_new_user(user=user, db=db)
    return user


def create_fail_test_user(db: Session):
    user = UserIn(
        first_name="rohan",
        last_name="m",
        age=28,
        gender="male",
        phone_number="123-124-2330",
        email="fail@test.co",
        address_line_one="123",
        address_line_two="st",
        city="SF",
        state="CA",
        country="USA",
        pincode="12345",
        birthdate="1994-04-29",
        password="fake",
    )
    user = create_new_user(user=user, db=db)
    return user


def create_test_accounts(user_id, db: Session):
    account1 = AccountOut(
        customer_id=user_id, current_balance=1000000, account_type="saving"
    )
    account2 = AccountOut(
        customer_id=user_id, current_balance=1000, account_type="checking"
    )

    a1 = create_new_account(account=account1, db=db)
    a2 = create_new_account(account=account2, db=db)
    return [a1, a2]
