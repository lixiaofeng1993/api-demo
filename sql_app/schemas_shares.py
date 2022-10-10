#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
# 创 建 人: 李先生
# 文 件 名: schemas_shares.py
# 创建时间: 2022/10/10 0010 20:20
# 版   本：V 0.1
# 说   明: 
"""
from pydantic import BaseModel


class SharesBase(BaseModel):
    id: str
    name: str
    code: str
    date: str
    open_price: str
    close_price: str
    down_price: str
    high_price: str
    amount: str
    forehead: str
    amplitude: str
    rise_fall: str
    increase_decrease: str
    turnover_rate: str

    class Config:
        orm_mode = True
