#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
# 创 建 人: 李先生
# 文 件 名: crud_shares.py
# 创建时间: 2022/10/10 0010 20:19
# 版   本：V 0.1
# 说   明: 
"""
from sqlalchemy.orm import Session

from sql_app.models import Shares
from sql_app.schemas_shares import SharesBase


def create_shares(db: Session, shares: SharesBase):
    db_shares = Shares(**shares.dict())
    db.add(db_shares)
    db.commit()
    db.refresh(db_shares)
    return db_shares
