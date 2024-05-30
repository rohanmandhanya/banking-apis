from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import Session
from uuid import uuid4

from db.base_class import BaseModel
from schemas import UserIn


class User(BaseModel):

    id = Column(Integer, primary_key=True, nullable=False)
    customer_id = Column(String(63), unique=True, nullable=False)

    first_name = Column(String(20), unique=False, nullable=False)
    last_name = Column(String(20), unique=False, nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    phone_number = Column(String(12), unique=True, nullable=False)
    birthdate = Column(String(63), unique=False, nullable=False)
    gender = Column(String(8), unique=False, nullable=False)
    line_one = Column(String(50), unique=False, nullable=False)
    line_two = Column(String(50), unique=False, nullable=False)
    city = Column(String(20), unique=False, nullable=False)
    state = Column(String(20), unique=False, nullable=False)
    country = Column(String(20), unique=False, nullable=False)
    pincode = Column(String(5), unique=False, nullable=False)
    password = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)


def create_new_user(user: UserIn, db: Session):

    user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        age=user.age,
        email=user.email,
        phone_number=user.phone_number,
        birthdate=user.birthdate,
        gender=user.gender,
        line_one=user.address_line_one,
        line_two=user.address_line_two,
        city=user.city,
        state=user.state,
        country=user.country,
        pincode=user.pincode,
        customer_id=str(uuid4()),
        password=user.password,
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(customer_id: str, db: Session):

    user = db.query(User).filter(User.customer_id == customer_id).first()
    return user


def check_user(email: str, db: Session):

    user = db.query(User).filter(User.email == email).first()
    return user
