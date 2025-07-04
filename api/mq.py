import aio_pika
import json
from config import settings


async def publish_task(task_id: str):
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps({"task_id": task_id}).encode()),
            routing_key=settings.RABBITMQ_QUEUE_NAME,
        )
