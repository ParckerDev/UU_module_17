from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .task import Task
from backend.db_depend import get_db
from typing import Annotated
from models import User
from schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify


router = APIRouter(prefix='/user', tags=['USER'])


@router.get('/')
async def get_all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User).where(User.username != None)).all()
    return users

@router.get('/user_id')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id):
    user = db.scalars(select(User).where(User.id == user_id)).one_or_none()
    if user:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    
@router.get('/user_id/tasks')
async def get_tasks_by_user_id(db: Annotated[Session, Depends(get_db)], user_id):
    tasks = db.scalars(select(Task).where(Task.user_id == user_id)).all()
    return tasks


@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    user = db.scalars(select(User).where(User.username == create_user.username)).one_or_none()
    if not user:
        db.execute(insert(User).values(username=create_user.username,
                                       firstname=create_user.firstname,
                                       lastname=create_user.lastname,
                                       age=create_user.age,
                                       slug=slugify(create_user.username)))
        db.commit()
        return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}
    else:
        return {'status_code': status.HTTP_404_NOT_FOUND, 'transaction': 'Failed'}
    

@router.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, update_user: UpdateUser):
    user = db.scalars(select(User).where(User.id == user_id)).one()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    db.execute(update(User).where(User.id == user_id).values(
        firstname=update_user.firstname,
        lastname=update_user.lastname,
        age=update_user.age
    ))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}

@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id):
    user = db.scalars(select(User).where(User.id == user_id)).one()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    db.execute(delete(User).where(User.id == user_id))
    db.execute(delete(Task).where(Task.user_id == user_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User and Tasks delete is successful!'}