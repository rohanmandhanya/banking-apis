from fastapi import FastAPI
import logging

from db import BaseModel, engine
from pre_populate import pre_populate
from apis import all_router
import time


def start_app():

    app = FastAPI(redoc_url="/documentation")
    BaseModel.metadata.create_all(bind=engine)
    app.include_router(
        all_router,
        prefix="/api",
        responses={404: {"description": "Not found"}},
    )

    time.sleep(5)
    pre_populate()

    return app


app = start_app()


@app.get("/", include_in_schema=False)
def hello_world():
    logging.info("App running fine")
    return {"message": "Hello World"}
