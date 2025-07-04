from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from uuid import UUID
from datetime import datetime

import models, schemas

async def create_task(db: AsyncSession, task_data: schemas.TaskCreate) -> models.Task:
    task = models.Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        status="pending"
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def get_task(db: AsyncSession, task_id: UUID) -> models.Task | None:
    result = await db.execute(select(models.Task).where(models.Task.id == task_id))
    return result.scalar_one_or_none()

async def list_tasks(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[models.Task]:
    result = await db.execute(select(models.Task).offset(skip).limit(limit))
    return result.scalars().all()

async def update_task_status(db: AsyncSession, task_id: UUID, status: str):
    stmt = update(models.Task).where(models.Task.id == task_id).values(
        status=status,
        started_at=datetime.utcnow() if status == "processing" else None,
        completed_at=datetime.utcnow() if status == "completed" else None
    )
    await db.execute(stmt)
    await db.commit()
