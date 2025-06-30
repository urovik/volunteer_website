from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI


from src.database.config import  init_db

from src.users.router import user_router
from src.auth.router import auth_router
from src.requests.router import request_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(request_router)



if __name__ == "__main__":
    uvicorn.run("src.main:app",reload = True)

