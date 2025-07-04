from pydantic import BaseModel
from uuid import UUID
from typing import Optional, Literal
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: Optional[str]
    priority: Literal["high", "medium", "low"]

class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    priority: Literal["high", "medium", "low"]
    status: Literal["pending", "processing", "completed", "failed"]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]

    class Config:
        orm_mode = True
