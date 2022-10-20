#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: models.py
# 说   明: 
# 创建时间: 2021/12/25 11:36
# @Version：V 0.1
# @desc :
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from sql_app.database import Base
from public.public import get_id


class User(Base):
    __tablename__ = "users"

    id = Column(String(32), default=get_id, primary_key=True, index=True)  # unique 同一个表中不能有相同的值
    name = Column(String(20), index=True)
    zh_name = Column(String(20), default=None)
    email = Column(String(50), default=None)
    hashed_password = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_delete = Column(Boolean, default=False)
    description = Column(Text, default=None)
    last_login = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    create_date = Column(DateTime, default=datetime.now)

    project = relationship("Project", back_populates="users")


class Sign(Base):
    __tablename__ = "sign"

    # id = Column(Integer, primary_key=True, index=True)
    id = Column(String(32), default=get_id, primary_key=True, index=True)
    name = Column(String(20), index=True)
    sign_type = Column(String(20), index=True)
    description = Column(Text, default=None)
    is_delete = Column(Boolean, default=False)
    update_date = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    create_date = Column(DateTime, default=datetime.now)

    users_id = Column(String(32), ForeignKey("users.id"))

    project = relationship("Project", back_populates="sign")


class Project(Base):
    __tablename__ = "project"

    id = Column(String(32), default=get_id, primary_key=True, index=True)
    name = Column(String(20), index=True)
    description = Column(Text, default=None)
    is_delete = Column(Boolean, default=False)
    update_date = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    create_date = Column(DateTime, default=datetime.now)

    users_id = Column(String(32), ForeignKey("users.id"))
    sign_id = Column(String(32), ForeignKey("sign.id"))

    sign = relationship("Sign", back_populates="project")
    users = relationship("User", back_populates="project")


class Author(Base):
    __tablename__ = "author"

    id = Column(String(32), default=get_id, primary_key=True, index=True)
    name = Column(String(20), index=True)  # 名字
    dynasty = Column(String(20), index=True)  # 朝代
    introduce = Column(Text, default=None)  # 介绍
    is_delete = Column(Boolean, default=False)
    update_date = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    create_date = Column(DateTime, default=datetime.now)

    poetry = relationship("Poetry", back_populates="author")


class Poetry(Base):
    __tablename__ = "poetry"

    id = Column(String(32), default=get_id, primary_key=True, index=True)
    type = Column(String(20), index=True)  # 类型
    phrase = Column(String(200), index=True)  # 名句
    explain = Column(Text, default=None)  # 解释
    appreciation = Column(Text, default=None)  # 赏析
    name = Column(String(200), index=True)  # 名字
    original = Column(Text, default=None)  # 原文
    translation = Column(Text, default=None)  # 译文
    background = Column(Text, default=None)  # 背景
    url = Column(String(200), default=None)  # 地址
    is_delete = Column(Boolean, default=False)
    update_date = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    create_date = Column(DateTime, default=datetime.now)

    author_id = Column(String(32), ForeignKey("author.id"), default=None)
    author = relationship("Author", back_populates="poetry")


class Shares(Base):
    __tablename__ = "shares"

    id = Column(String(32), default=get_id, primary_key=True, index=True)
    name = Column(String(200), index=True)  # 股票名称
    code = Column(String(200), index=True)  # 股票代码
    date_time = Column(DateTime, index=True)  # 日期
    open_price = Column(String(200), index=True)  # 开盘
    new_price = Column(String(200), index=True)  # 收盘
    top_price = Column(String(200), index=True)  # 最高
    down_price = Column(String(200), index=True)  # 最低
    turnover = Column(String(200), index=True)  # 成交量
    business_volume = Column(String(200), index=True)  # 成交额
    amplitude = Column(String(200), index=True)  # 振幅
    rise_and_fall = Column(String(200), index=True)  # 涨跌幅
    rise_and_price = Column(String(200), index=True)  # 涨跌额
    turnover_rate = Column(String(200), index=True)  # 换手率

    is_delete = Column(Boolean, default=False)
    update_date = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    create_date = Column(DateTime, default=datetime.now)
