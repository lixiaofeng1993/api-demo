#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: public.py
# 说   明: 
# 创建时间: 2021/12/27 21:12
# @Version：V 0.1
# @desc :
import uuid
import json
from sql_app.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from datetime import datetime

from public.res_sign import encrypt
from public.custom_code import result, page


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_id():
    return uuid.uuid4().hex


def format_time(data):
    if hasattr(data, "sign"):
        data.sign = format_time(data.sign)
    if hasattr(data, "users"):
        data.users = format_time(data.users)
    if hasattr(data, "last_login"):
        if isinstance(data.last_login, datetime):
            setattr(data, "last_login", data.last_login.strftime("%Y-%m-%d %H:%M:%S"))
    if hasattr(data, "create_date"):
        if isinstance(data.create_date, datetime):
            setattr(data, "create_date", data.create_date.strftime("%Y-%m-%d %H:%M:%S"))
    if hasattr(data, "update_date"):
        if isinstance(data.update_date, datetime):
            setattr(data, "update_date", data.update_date.strftime("%Y-%m-%d %H:%M:%S"))
    return data


def json_format(data):
    if isinstance(data, list):
        json_list = list()
        for d in data:
            d = jsonable_encoder(format_time(d))
            json_list.append(d)
        # result["result"] = encrypt(json.dumps(json_list, ensure_ascii=False))
        result["result"] = json_list
    else:
        # data = json.dumps(jsonable_encoder(format_time(data)), ensure_ascii=False)
        # result["result"] = encrypt(data)
        result["result"] = format_time(data)
    return result
