from pydantic import BaseModel, Field, validator
from enum import Enum


class AccountType(Enum):

    saving = "saving"
    checking = "checking"


class TransactionType(Enum):

    debit = "debit"
    credit = "credit"


class AccountIn(BaseModel):

    account_type: AccountType = Field(
        description="What type of account you want to open, Currently only two options available"
    )
    deposit: int = Field(
        gt=0,
        description="It's the initial amount when opening an account, must be positive",
    )

    @validator("deposit", pre=True)
    @classmethod
    def valid_amount(cls, value):
        if value <= 0:
            raise ValueError("Deposit can't be less than or equal to zero")

        return value


class AccountOut(BaseModel):

    customer_id: str = Field(
        description="User id under which the account is been created"
    )
    account_type: AccountType = Field(description="Type of account")
    current_balance: int = Field(description="It's your current account balance")

    class Config:
        use_enum_values = True


# This will always create two entry for both account where it credit happen and debit happen
class Transaction(BaseModel):

    account_id: str = Field(description="Account id you want to use for transaction")
    transaction_amount: int = Field(
        description="How much you want to send to 3rd party account, Needs to minimum value of 1",
    )
    transaction_type: TransactionType = Field(description="Type of Transaction")
    account_third_party: str = Field(
        description="Account id you want to transfer the amount"
    )
    created_at: str = Field(description="Time and date at which the transaction occur")

    class Config:
        use_enum_values = True


class TransactionIn(BaseModel):

    to_account: str = Field(description="From the account you want to make transfer")
    from_account: str = Field(description="To the account you want to make transfer")
    amount: int = Field(
        ge=1,
        description="How much you want to send to 3rd party account, Needs to minimum value of 1",
    )

    @validator("amount", pre=True)
    @classmethod
    def valid_amount(cls, value):
        if value <= 0:
            raise ValueError("Amount can't be less than or equal to zero")

        return value
