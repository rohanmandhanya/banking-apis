from db.models.users import User
from db import engine
from uuid import uuid4
from sqlalchemy.orm import sessionmaker
import sys, os


def pre_populate():

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = SessionLocal()

    user = db.query(User).filter().first()

    if not user:

        user1 = User(
            first_name="fake",
            last_name="user",
            age=30,
            email="fake@test.com",
            phone_number="123-123-1234",
            birthdate="1996-25-12",
            gender="male",
            line_one="123",
            line_two="st",
            city="munich",
            state="bavaria",
            country="germany",
            pincode="12345",
            customer_id="123456",
            password="fake",
        )

        db.add(user1)

        db.commit()
