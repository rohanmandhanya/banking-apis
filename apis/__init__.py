from apis import users
from apis import accounts

from fastapi import APIRouter


all_router = APIRouter()

all_router.include_router(users.router, prefix="/user", tags=["users"])
all_router.include_router(accounts.router, prefix="/account", tags=["accounts"])
