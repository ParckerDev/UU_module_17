from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depend import get_db
from typing import Annotated
from models import Task, User
from schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix='/task', tags=['TASK'])


@router.get('/')
async def get_all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task).where(Task.id != 0)).all()
    return tasks

@router.get('/task_id')
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalars(select(Task).where(Task.id == task_id)).one_or_none()
    if task:
        return task
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found'
        )
    

@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], user_id: int, new_task: CreateTask):
    user = db.scalars(select(User).where(User.id == user_id)).one_or_none()
    if user:
        db.execute(insert(Task).values(
            title=new_task.title,
            content=new_task.content,
            priority=new_task.priority,
            user_id=user_id,
            slug=slugify(new_task.title)
        ))

@router.put('/update')
async def update_task(db: Annotated[Session, Depends(get_db)], task_id: int, update_task: UpdateTask):
    task = db.scalars(select(Task).where(Task.id == task_id)).one()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='task was not found'
        )
    db.execute(update(Task).where(Task.id == task.id).values(
        title=update_task.title,
        content=update_task.content,
        priority=update_task.priority
    ))

@router.delete('/delete')
async def delete_task():
    pass