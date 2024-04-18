from contextlib import asynccontextmanager
from src.adapters.mysql_adapter import create_db, get_db_session
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.controllers.countries import CountryCRUD
from src.routes import user, entity, position, nps
import uvicorn
from src.utils.logger import logger
from src.utils.settings import (
    APP_PORT
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Start Service...")
    create_db()

    generator = get_db_session()
    session = next(generator)
    logger.info("loading countries...")
    country_crud_instance = CountryCRUD()
    country_crud_instance.load_countries(session)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return {"message": "Hello World from docker"}


# add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


app.include_router(
    user.router,
    prefix="/user",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    entity.router,
    prefix="/entity",
    tags=["entity"],
    responses={404: {"description": "Not found"}}
)

app.include_router(
    position.router,
    prefix="/position",
    tags=["position"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    nps.router,
    prefix="/nps",
    tags=["nps"],
    responses={404: {"description": "Not found"}},
)

if __name__ == "__main__":
    logger.info("Start service on port {APP_PORT}")
    uvicorn.run(app, host="0.0.0.0", port=APP_PORT or 8000)

