#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: crud_sign.py
# 说   明: 
# 创建时间: 2021/12/31 19:52
# @Version：V 0.1
# @desc :
from sqlalchemy.orm import Session

from sql_app.models import Sign
from sql_app.schemas_sign import SignCreate


def get_sign(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Sign).offset(skip).limit(limit).all()


def get_sign_by_id(db: Session, sign_id: str):
    return db.query(Sign).filter(Sign.id == sign_id).first()


def get_sign_by_name(db: Session, name: str):
    return db.query(Sign).filter(Sign.name == name).first()


def create_sign(db: Session, sign: SignCreate):
    db_sign = Sign(**sign.dict())
    db.add(db_sign)
    db.commit()
    db.refresh(db_sign)
    return db_sign
