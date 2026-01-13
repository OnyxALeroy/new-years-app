from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.crud.user import user_crud
from app.routes import auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    await user_crud.create_admin_user()
    yield
    await close_mongo_connection()


app = FastAPI(
    title="New Year's Event API",
    description="API for organizing New Year's events",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "New Year's Event API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}