import asyncio
import json
import signal
from datetime import datetime
from aio_pika import connect_robust, IncomingMessage
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.database import AsyncSessionLocal
from api.models import Task, TaskStatus
from api.logger import setup_logger
from api.config import settings




logger = setup_logger("worker")

async def process_task(session: AsyncSession, task_id: str):
    stmt = select(Task).where(Task.id == task_id)
    result = await session.execute(stmt)
    task = result.scalar_one_or_none()

    if not task:
        logger.error(f"Task with id {task_id} not found.")
        return
    task.status = TaskStatus.processing
    task.started_at = datetime.now()
    await session.commit()
    logger.info(f"Started processing task {task.id}: {task.title}")
    await asyncio.sleep(settings.WORKER_TIMEOUT)
    task.status = TaskStatus.completed
    task.completed_at = datetime.now()
    await session.commit()
    logger.info(f"Completed task {task.id}: {task.title}")

async def on_message(message: IncomingMessage):
    async with message.process():
        try:
            data = json.loads(message.body.decode())
            task_id = data.get("task_id")
            logger.info(f"Received task ID: {task_id}")

            async with AsyncSessionLocal() as session:
                await process_task(session, task_id)
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)


async def worker():
    connection = await connect_robust(settings.RABBITMQ_URL)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)
    queue = await channel.declare_queue(settings.RABBITMQ_QUEUE_NAME, durable=True)
    await queue.consume(on_message)
    logger.info("Worker started and waiting for messages...")
    stop_event = asyncio.Event()

    def shutdown():
        logger.info("Received shutdown signal")
        stop_event.set()

    for sig in [signal.SIGINT, signal.SIGTERM]:
        asyncio.get_running_loop().add_signal_handler(sig, shutdown)

    await stop_event.wait()

    logger.info("Shutting down gracefully...")
    await connection.close()


if __name__ == "__main__":
    logger.info("Initializing database...")
    logger.info("Starting worker service...")
    try:
        asyncio.run(worker())
    except KeyboardInterrupt:
        logger.info("Worker stopped by user.")
