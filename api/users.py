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

from fastapi import Depends, APIRouter, HTTPException, status, Request, Body
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sql_app.schemas_users import UserToken, UserCreate, User
from sql_app import crud_users
from sql_app.database import Base, engine
from dependencies import get_current_user, verify_password
from public.jwt_sign import create_access_token
from public.public import get_db, json_format
from conf.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from public import exception
from public import field_check

Base.metadata.create_all(bind=engine)  # 生成数据库

router = APIRouter()


@router.post("/register", summary="注册接口", description="这是一个注册接口")
async def register(request: Request, user_create: UserCreate, db: Session = Depends(get_db)):
    field_check.check_name(user_create.name)
    field_check.check_zh_name(user_create.zh_name)
    field_check.check_password(user_create.hashed_password)
    field_check.check_email(user_create.email)
    db_name = crud_users.get_user_by_name(db, name=user_create.name)
    db_email = crud_users.get_user_by_email(db, email=user_create.email)
    if db_name:
        raise exception.AlreadyExistException(name="name")
    if db_email:
        raise exception.AlreadyExistException(name="email")
    user = crud_users.create_user(db=db, user=user_create)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.name}, expires_delta=access_token_expires)
    await request.app.state.redis.setex(key=user.name, value=access_token, seconds=ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    user.access_token = access_token
    return json_format(user)


@router.post("/login", summary="登录接口", description="这是一个登录接口")
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
    await request.app.state.redis.setex(key=username, value=access_token, seconds=ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    db_user.access_token = access_token
    crud_users.set_last_login(db, user_id=db_user.id)
    return json_format(db_user)


@router.get("/me", summary="获取当前登录用户信息")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return json_format(current_user)


@router.get("/", summary="获取所有用户信息")
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                     user: User = Depends(get_current_user)):
    users = crud_users.get_users(db, skip=skip, limit=limit)
    if users is None:
        raise exception
    return json_format(users)


@router.get("/{user_id}", summary="获取指定用户信息")
async def read_user(user_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_user = crud_users.get_user(db, user_id=user_id)
    if db_user is None:
        raise exception.NotExitException(name=f"ID {user_id}")
    return json_format(db_user)


@router.put("/super/{user_id}", response_model=User, summary="修改用户权限为管理员")
async def set_super_user(user_id: str, verify_code=None, db: Session = Depends(get_db),
                         user: User = Depends(get_current_user)):
    if not verify_code == "8023":
        super_user = crud_users.get_super_user(db, user.id)
        if super_user is None:
            raise exception.NotSuperUserException
    db_user = crud_users.get_user(db, user_id=user_id)
    if db_user is None:
        raise exception.NotExitException(name=f"ID {user_id}")
    crud_users.set_super_user(db, user_id=user_id)
    super_user = crud_users.get_super_user(db, user_id)
    return json_format(super_user)


@router.delete("/{user_id}", summary="删除指定用户信息")
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
    return json_format(db_user)


@router.post("/logout", summary="退出登录")
async def logout(request: Request, user: User = Depends(get_current_user)):
    access_token = await request.app.state.redis.get(user.name)
    if not access_token:
        raise exception.LogoutException(name=user.name)
    await request.app.state.redis.delete(key=user.name)
    raise exception.LogoutResponse(name=user.name)
