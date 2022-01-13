#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: schemas.py
# 说   明: 
# 创建时间: 2021/12/25 11:40
# @Version：V 0.1
# @desc :
from typing import List, Optional, Dict, Text
from datetime import datetime
from pydantic import BaseModel

from sql_app.schemas_sign import Sign, User


class ProjectBase(BaseModel):
    name: str
    description: Text


class ProjectCreate(ProjectBase):
    sign_id: str = ""
    users_id: str = ""


class Project(ProjectBase):
    id: str
    is_delete: bool = False
    update_date: datetime
    create_date: datetime
    sign: Optional[Sign] = {}
    users: Optional[User] = {}

    class Config:
        orm_mode = True
