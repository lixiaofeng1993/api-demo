#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: public.py
# 说   明: 
# 创建时间: 2021/12/27 21:12
# @Version：V 0.1
# @desc :

from sql_app.database import SessionLocal
import uuid


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_id():
    return uuid.uuid4().hex
