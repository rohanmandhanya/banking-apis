from pydantic import BaseModel, Field, validator
from typing import Optional
from enum import Enum
import datetime


class Gender(Enum):

    male = "male"
    female = "female"
    other = "other"


class UserIn(BaseModel):

    first_name: str = Field(
        description="User First Name. Must be an String value. Limit 20 characters"
    )
    last_name: str = Field(
        description="User Last Name. Must be an String value. Limit 20 characters"
    )
    age: int = Field(
        le=120, ge=15, description="User age. Must be an integer value"
    )  # TODO: 15 < age < 120
    gender: Gender = Field(description="User Gender. Choose from the options given")
    phone_number: str = Field(
        description="User Phone number. Must been in the format `000-000-0000` and needs to be 10 digit phone number",
    )
    email: str = Field(
        description="User Email address. It should follow the email format correctly",
    )
    address_line_one: str = Field(
        description="User Address, Line one of there Street address",
    )
    address_line_two: Optional[str] = Field(
        description="User Address, Line two of there Street address. It can be empty",
    )
    city: str = Field(
        description="User Address, City of there Street address",
    )
    state: str = Field(
        description="User Address, State of there Street address",
    )
    country: str = Field(
        description="User Address,Country of there Street address",
    )
    pincode: str = Field(
        description="User Address, Pincode of there Street address. Must be a valid pincode `[4,6]` digits",
    )
    birthdate: datetime.date = Field(
        description="User Date of birth, must be a date and format `YYYY-MM-DD`",
    )
    password: str = Field(
        description="Choose your secret and share with up 😉",
    )

    @validator("phone_number", pre=True)
    @classmethod
    def valid_phone(cls, value):
        if len(value) != 12:
            raise ValueError("Wrong phone number")
        return value

    @validator("age", pre=True)
    @classmethod
    def valid_age(cls, value):
        if 15 > value:
            raise ValueError("Too young to have an account")
        elif value > 150:
            raise ValueError("Hello Immortals!!!!")

        return value

    @validator("pincode", pre=True)
    @classmethod
    def valid_pincode(cls, value):
        if len(value) > 7 and len(value) < 3:
            raise ValueError("Pincode is invalid")

        return value

    @validator("email", pre=True)
    @classmethod
    def valid_email(cls, value):
        if "@" not in value or "." not in value:
            raise ValueError("Email is invalid")

        return value

    class Config:
        use_enum_values = True


class UserOut(BaseModel):

    id: int
    first_name: str
    last_name: str
    email: str
    age: int = Field(lt=120)
    gender: Gender


class AccessToken(BaseModel):

    access_token: str
    token_type: str = "bearer"
