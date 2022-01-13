#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: schemas.py
# 说   明: 
# 创建时间: 2021/12/25 11:40
# @Version：V 0.1
# @desc :
from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    zh_name: str = None
    email: str
    description: str


class UserCreate(UserBase):
    hashed_password: str


class User(UserBase):
    id: str
    is_delete: bool = False
    is_active: bool = True
    is_superuser: bool = False
    last_login: datetime
    create_date: datetime

    class Config:
        orm_mode = True


class UserToken(User):
    access_token: str = None
