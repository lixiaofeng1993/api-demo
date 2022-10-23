#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: sign.py
# 说   明: 
# 创建时间: 2021/12/26 19:21
# @Version：V 0.1
# @desc :

from typing import List

from fastapi import Depends, APIRouter, Body
from sqlalchemy.orm import Session

from sql_app.schemas_sign import Sign, SignCreate, User
from sql_app import crud_sign
from public import exception
from public import field_check
from dependencies import get_current_user_info

from public.common import get_db, json_format

router = APIRouter()


@router.post("/", summary="创建加密方式接口")
async def create_sign(sign: SignCreate, db: Session = Depends(get_db),
                      user: User = Depends(get_current_user_info)):
    field_check.check_name(sign.name)
    field_check.check_name(sign.sign_type)
    db_user = crud_sign.get_sign_by_name(db, name=sign.name)
    if db_user:
        raise exception.AlreadyExistException(name=sign.name)
    sign.users_id = user.id
    return json_format(crud_sign.create_sign(db=db, sign=sign))


@router.get("/", summary="获取所有加密信息")
def read_sign(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud_sign.get_sign(db, skip=skip, limit=limit)
    return json_format(users)


@router.get("/{sign_id}", summary="获取指定加密信息")
def read_user(sign_id: str, db: Session = Depends(get_db)):
    db_user = crud_sign.get_sign_by_id(db, sign_id=sign_id)
    if db_user is None:
        raise exception.NotExitException(name=f"ID {sign_id}")
    return json_format(db_user)
