#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: schemas.py
# 说   明: 
# 创建时间: 2021/12/25 11:40
# @Version：V 0.1
# @desc :
from typing import List, Optional, Dict, Text
from pydantic import BaseModel

from sql_app.schemas_users import User


class SignBase(BaseModel):
    name: str
    sign_type: str
    description: Text


class SignCreate(SignBase):
    users_id: str = ""


class Sign(SignBase):
    id: str
    is_delete: bool = False
    update_date: str
    create_date: str

    class Config:
        orm_mode = True
