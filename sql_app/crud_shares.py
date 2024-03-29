#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: crud_shares.py
# 创建时间: 2022/10/20 0020 19:20
# @Version：V 0.1
# @desc :
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct

from sql_app.models import Shares


def get_shares_by_name(db: Session, name: str, flag=False):
    if flag:
        return db.query(Shares).filter(Shares.name == name, Shares.is_delete == 0).order_by(
            Shares.date_time.asc()).first()
    else:
        return db.query(Shares).filter(Shares.name == name, Shares.is_delete == 0).order_by(
            Shares.date_time.desc()).first()


def get_shares_avg(db: Session, name: str):
    max_num = db.query(func.max(Shares.top_price)).filter(Shares.name == name, Shares.is_delete == 0).scalar()
    min_num = db.query(func.min(Shares.down_price)).filter(Shares.name == name, Shares.is_delete == 0).scalar()
    avg_num = db.query(func.avg(Shares.new_price)).filter(Shares.name == name, Shares.is_delete == 0).scalar()
    max_num = round(float(max_num), 2) if max_num else 0
    min_num = round(float(min_num), 2) if min_num else 0
    avg_num = round(float(avg_num), 2) if avg_num else 0
    return max_num, min_num, avg_num


def get_shares_days(db: Session, name: str):
    day_list = db.query(distinct(Shares.date_time)).filter(Shares.name == name, Shares.is_delete == 0).all()
    return day_list


def get_shares_code(db: Session, code: str):
    return db.query(Shares).filter(Shares.code == code, Shares.is_delete == 0).first()


def add_all_shares(db: Session, shares_list: list):
    case = []
    for shares in shares_list:
        db_shares = Shares(
            name=shares["name"],
            code=shares["code"],
            date_time=shares["date_time"],
            open_price=shares["open_price"],
            new_price=shares["new_price"],
            top_price=shares["top_price"],
            down_price=shares["down_price"],
            turnover=shares["turnover"],
            business_volume=shares["business_volume"],
            amplitude=shares["amplitude"],
            rise_and_fall=shares["rise_and_fall"],
            rise_and_price=shares["rise_and_price"],
            turnover_rate=shares["turnover_rate"],
        )
        case.append(db_shares)
    db.add_all(case)
    db.commit()
