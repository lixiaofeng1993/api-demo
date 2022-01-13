#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: crud_project.py
# 说   明: 
# 创建时间: 2021/12/31 19:53
# @Version：V 0.1
# @desc :
from sqlalchemy.orm import Session

from sql_app.models import Project
from sql_app.schemas_project import ProjectCreate


def get_project(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Project).offset(skip).limit(limit).all()


def get_project_by_id(db: Session, project_id: str):
    return db.query(Project).filter(Project.id == project_id).first()


def get_project_by_name(db: Session, name: str):
    return db.query(Project).filter(Project.name == name).first()


def create_project(db: Session, project: ProjectCreate):
    db_project = Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project
