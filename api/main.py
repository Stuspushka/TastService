from contextlib import asynccontextmanager

from dotenv import load_dotenv
load_dotenv()
import aio_pika
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from aio_pika.exceptions import AMQPConnectionError
from routers import router
from database import engine, AsyncSessionLocal, Base
from config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Task Processing API", lifespan=lifespan)

app.include_router(router)

@app.get("/health", tags=["Health"])
async def health_check():
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
    except SQLAlchemyError:
        return JSONResponse(status_code=503, content={"status": "error", "database": "disconnected"})
    try:
        connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        await connection.close()
    except AMQPConnectionError:
        return JSONResponse(status_code=503, content={"status": "error", "rabbitmq": "disconnected"})

    return {"status": "ok", "database": "connected", "rabbitmq": "connected"}
