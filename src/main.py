from contextlib import asynccontextmanager
from typing import Union

from fastapi import FastAPI
from api.db.db_session import init_db
from api.events.routing import router as students_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # before app startup up
    init_db()
    yield
    # clean up


app = FastAPI(lifespan=lifespan)

# include router
app.include_router(students_router)