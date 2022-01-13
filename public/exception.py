#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: exception.py
# 说   明: 
# 创建时间: 2021/12/27 22:52
# @Version：V 0.1
# @desc :

from fastapi import HTTPException, status


class TokenException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "token校验失败！"
        self.headers = {"WWW-Authenticate": "Bearer"}


class InactiveException(HTTPException):
    def __init__(self, status_code=status.HTTP_400_BAD_REQUEST, name=None):
        self.status_code = status_code
        self.detail = f" {name} 非活跃用户！"


class LoginRepeatException(HTTPException):
    def __init__(self, status_code=status.HTTP_400_BAD_REQUEST, name=None, token=None):
        token = token.decode() if token and isinstance(token, bytes) else None
        self.status_code = status_code
        self.detail = f" {name} 已登录！"
        self.headers = {"WWW-Authenticate": f"Bearer {token}"}


class PasswordExitException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "密码错误！"


class NotSuperUserException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "登录用户没有权限！"


class DeleteException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "删除失败！"


class NotExitException(HTTPException):
    def __init__(self, status_code=status.HTTP_400_BAD_REQUEST, name=None):
        self.status_code = status_code
        self.detail = f" {name} 不存在！"


class AlreadyExistException(HTTPException):
    def __init__(self, status_code=status.HTTP_400_BAD_REQUEST, name=None):
        self.status_code = status_code
        self.detail = f" {name} 已存在！"


class CheckFieldException(HTTPException):
    def __init__(self, status_code=status.HTTP_400_BAD_REQUEST, name=None, patt=None):
        self.status_code = status_code
        self.detail = f"{name} 不符合格式 {patt}"
