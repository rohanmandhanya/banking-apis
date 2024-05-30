from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from jose import jwt
from jose import JWTError
from typing import Annotated

from db.database import get_db
from db.models.users import create_new_user, get_user, check_user
from core.config import settings
from core.security import create_access_token
from schemas import UserIn, UserOut, AccessToken


router = APIRouter()


@router.post("/create", response_model=UserOut)
def create_user(userinfo: UserIn, db: Session = Depends(get_db)):
    """
    This api is used to create user(customer), we create accounts under user and has multiple features which requires authentication.
    """
    # TODO: Add hashing to the code
    # userinfo.password = userinfo.password
    user = create_new_user(userinfo, db)
    return UserOut(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        age=user.age,
        gender=user.gender,
        email=user.email,
    )


@router.post("/login", response_model=AccessToken)
def user_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    """
    This api is used to login user(customer), it creates a token which let's verification for 5 hours.
    It import fastapi form - REQUIRED `username(email)` AND `password`
    which you used while creating your user
    """

    user = check_user(form_data.username, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    if user.password != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(user.customer_id)
    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")


def get_customer(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized User",
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        c_id: str = payload.get("customer_id")
        if c_id is None:
            raise token_exception
    except JWTError:
        raise token_exception

    user = get_user(c_id, db)

    if not user:
        raise token_exception

    return UserOut(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        age=user.age,
        gender=user.gender,
        email=user.email,
    )
