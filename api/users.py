#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: users.py
# 说   明: 
# 创建时间: 2021/12/25 13:40
# @Version：V 0.1
# @desc :

from typing import List, Optional, Dict
from datetime import datetime, timedelta

from fastapi import Depends, APIRouter, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sql_app.schemas_users import UserToken, UserCreate, User
from sql_app import crud_users
from dependencies import get_current_user, verify_password
from public.jwt_sign import create_access_token
from public.public import get_db
from conf.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from public import exception
from public import field_check

router = APIRouter()


@router.post("/register", response_model=UserToken)
async def register(request: Request, user_create: UserCreate, db: Session = Depends(get_db)):
    field_check.check_name(user_create.name)
    field_check.check_zh_name(user_create.zh_name)
    field_check.check_password(user_create.hashed_password)
    field_check.check_email(user_create.email)
    db_name = crud_users.get_user_by_name(db, name=user_create.name)
    db_email = crud_users.get_user_by_email(db, email=user_create.email)
    if db_name or db_email:
        raise exception.AlreadyExistException(name="name 或者 email")
    user = crud_users.create_user(db=db, user=user_create)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.name}, expires_delta=access_token_expires)
    await request.app.state.redis.set(user.name, access_token, ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    user.access_token = access_token
    return user


@router.post("/login", response_model=UserToken)
async def login(request: Request, db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    db_user = crud_users.get_user_by_name(db, name=username)
    if not db_user:
        raise exception.NotExitException(name=username)
    if db_user.is_delete:
        raise exception.InactiveException(name=username)
    if not verify_password(password, db_user.hashed_password):
        raise exception.PasswordExitException
    cache_token = await request.app.state.redis.get(username)
    if cache_token:
        raise exception.LoginRepeatException(name=username, token=cache_token)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": username}, expires_delta=access_token_expires)
    await request.app.state.redis.set(username, access_token, ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    db_user.access_token = access_token
    return db_user


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                     user: User = Depends(get_current_user)):
    users = crud_users.get_users(db, skip=skip, limit=limit)
    if users is None:
        raise exception
    return users


@router.get("/{user_id}", response_model=User)
async def read_user(user_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_user = crud_users.get_user(db, user_id=user_id)
    if db_user is None:
        raise exception.NotExitException(name=f"ID {user_id}")
    return db_user


@router.put("/super/{user_id}", response_model=User)
async def set_super_user(user_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    super_user = crud_users.get_super_user(db, user.id)
    if super_user is None:
        raise exception.NotSuperUserException
    db_user = crud_users.get_user(db, user_id=user_id)
    if db_user is None:
        raise exception.NotExitException(name=f"ID {user_id}")
    crud_users.set_super_user(db, user_id=user_id)
    super_user = crud_users.get_super_user(db, user_id)
    return super_user


@router.delete("/{user_id}", response_model=User)
async def delete_user(user_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    super_user = crud_users.get_super_user(db, user.id)
    if super_user is None:
        raise exception.NotSuperUserException
    db_user = crud_users.get_user(db, user_id=user_id)
    if db_user is None:
        raise exception.NotExitException(name=f"ID {user_id}")
    crud_users.delete_user(db, user_id=user_id)
    db_user = crud_users.get_delete_user(db, user_id)
    if db_user is None:
        raise exception.DeleteException
    return db_user
