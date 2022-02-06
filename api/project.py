#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: project.py
# 说   明: 
# 创建时间: 2021/12/25 23:53
# @Version：V 0.1
# @desc :
from typing import List, Dict

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from sql_app.schemas_project import Project, ProjectCreate, User
from sql_app import crud_project, crud_sign
from public import exception
from public import field_check
from dependencies import get_current_user_info

from public.public import get_db, json_format

router = APIRouter()


@router.post("/", response_model=Project, summary="创建项目接口")
async def create_project(project: ProjectCreate, db: Session = Depends(get_db),
                         user: User = Depends(get_current_user_info)):
    field_check.check_name(project.name)
    db_user = crud_project.get_project_by_name(db, name=project.name)
    if db_user:
        raise exception.AlreadyExistException(name=project.name)
    project.users_id = user.id
    sign_user = crud_sign.get_sign_by_id(db, project.sign_id)
    if not sign_user:
        raise exception.CheckIDException(name="sign", patt=project.sign_id)
    return json_format(crud_project.create_project(db=db, project=project))


@router.get("/", response_model=List[Project], summary="获取所有项目信息")
def read_project(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud_project.get_project(db, skip=skip, limit=limit)
    return json_format(users)


@router.get("/{project_id}", response_model=Project, summary="获取指定项目信息")
def read_user(project_id: str, db: Session = Depends(get_db)):
    db_user = crud_project.get_project_by_id(db, project_id=project_id)
    if db_user is None:
        raise exception.NotExitException(name=f"ID {project_id}")
    return json_format(db_user)
