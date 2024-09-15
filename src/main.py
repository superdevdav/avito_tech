import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.schemas.db.init_db import create_tables
from src.routing.common import common_router
from src.routing.tenders import tenders_router
from src.routing.bids import bids_router

@asynccontextmanager
async def lifespan(app: FastAPI):
      await create_tables()
      print('INFO:     База данных создана')
      yield
      print('INFO:     Выключение')

app = FastAPI(
      lifespan=lifespan, 
      root_path="/api"
)

app.include_router(router=common_router)
app.include_router(router=tenders_router)
app.include_router(router=bids_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)