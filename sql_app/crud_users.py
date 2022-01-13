#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: crud_users.py
# 说   明: 
# 创建时间: 2021/12/31 19:48
# @Version：V 0.1
# @desc :

from sqlalchemy.orm import Session

from sql_app.models import User
from sql_app.schemas_users import UserCreate
from public.jwt_sign import get_password_hash


def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id, User.is_delete == 0).first()


def get_delete_user(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id, User.is_delete == 1).first()


def get_super_user(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id, User.is_superuser == 1).first()


def get_user_by_name(db: Session, name: str):
    return db.query(User).filter(User.name == name, User.is_delete == 0).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email, User.is_delete == 0).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).filter(User.is_delete == 0).offset(skip).limit(
        limit).all()


def create_user(db: Session, user: UserCreate):
    fake_hashed_password = get_password_hash(user.hashed_password)
    db_user = User(
        email=user.email, hashed_password=fake_hashed_password, name=user.name, description=user.description,
        zh_name=user.zh_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def set_super_user(db: Session, user_id):
    db.query(User).filter(
        User.id == user_id,
        User.is_delete == 0,
        User.is_superuser == 0
    ).update({User.is_superuser: True})
    db.commit()
    db.close()


def delete_user(db: Session, user_id):
    db.query(User).filter(
        User.id == user_id,
        User.is_delete == 0,
        User.is_superuser == 0
    ).update({User.is_delete: True})
    db.commit()
    db.close()
