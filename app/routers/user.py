from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depend import get_db
from typing import Annotated
from models import User
from schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify


router = APIRouter(prefix='/user', tags=['USER'])


@router.get('/')
async def get_all_users():
    pass

@router.get('/user_id')
async def user_by_id():
    pass

@router.post('/create')
async def create_user():
    pass

@router.put('/update')
async def update_user():
    pass

@router.delete('/delete')
async def delete_user():
    pass