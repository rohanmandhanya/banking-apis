from datetime import datetime
from datetime import timedelta
from typing import Optional

from core.config import settings
from jose import jwt


# TODO: we can add password and hash it
def password_hash():
    pass


def create_access_token(customer_id: str, expires_delta: Optional[timedelta] = None):

    to_encode = {"customer_id": customer_id}

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
