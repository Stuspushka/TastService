from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
import schemas
import crud
import database
import mq

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=schemas.TaskResponse)
async def create_task(task_data: schemas.TaskCreate, db: AsyncSession = Depends(database.get_db)):
    task = await crud.create_task(db, task_data)
    await mq.publish_task(str(task.id))
    return task


@router.get("/{task_id}", response_model=schemas.TaskResponse)
async def get_task(task_id: UUID, db: AsyncSession = Depends(database.get_db)):
    task = await crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/", response_model=list[schemas.TaskResponse])
async def list_tasks(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(database.get_db)):
    return await crud.list_tasks(db, skip=skip, limit=limit)
