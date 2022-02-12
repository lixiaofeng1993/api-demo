#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: exception.py
# 说   明: 
# 创建时间: 2021/12/27 22:52
# @Version：V 0.1
# @desc :

from fastapi import HTTPException, status

from public.custom_code import *


class TokenException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = {
            "code": EXCEPTION_TOKEN_CODE,
            "message": "token校验失败！"
        }
        self.headers = {"WWW-Authenticate": "Bearer"}


class InactiveException(HTTPException):
    def __init__(self, status_code=status.HTTP_200_OK, name=None):
        self.status_code = status_code
        self.detail = {
            "code": InactiveException,
            "message": f" {name} 非活跃用户！"
        }


class LoginRepeatException(HTTPException):
    def __init__(self, status_code=status.HTTP_200_OK, name=None, token=None):
        token = token.decode() if token and isinstance(token, bytes) else token
        self.status_code = status_code
        self.detail = {
            "code": EXCEPTION_LOGIN_CODE,
            "message": f" {name} 已登录！"
        }
        self.headers = {"WWW-Authenticate": f"Bearer {token}"}


class PasswordExitException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_200_OK
        self.detail = {
            "code": EXCEPTION_PASS_CODE,
            "message": "密码错误！"
        }


class NotSuperUserException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_200_OK
        self.detail = {
            "code": EXCEPTION_SUPER_CODE,
            "message": "登录用户没有权限！"
        }


class DeleteException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_200_OK
        self.detail = {
            "code": EXCEPTION_DELETE_CODE,
            "message": "删除失败！"
        }


class NotExitException(HTTPException):
    def __init__(self, status_code=status.HTTP_200_OK, name=None):
        self.status_code = status_code
        self.detail = {
            "code": EXCEPTION_NOT_EXIT_CODE,
            "message": f" {name} 不存在！"
        }


class AlreadyExistException(HTTPException):
    def __init__(self, status_code=status.HTTP_200_OK, name=None):
        self.status_code = status_code
        self.detail = {
            "code": EXCEPTION_ALREADY_EXIST_CODE,
            "message": f" {name} 已存在！"
        }


class FormatFieldException(HTTPException):
    def __init__(self, status_code=status.HTTP_200_OK, name=None, patt=None):
        self.status_code = status_code
        self.detail = {
            "code": EXCEPTION_FORMAT_CODE,
            "message": f"{name} 不符合格式 {patt}"
        }


class CheckIDException(HTTPException):
    def __init__(self, status_code=status.HTTP_200_OK, name=None, patt=None):
        self.status_code = status_code
        self.detail = {
            "code": EXCEPTION_CHECK_CODE,
            "message": f"{name} ID {patt} 不存在！"
        }


class LogoutException(HTTPException):
    def __init__(self, status_code=status.HTTP_200_OK, name=None, patt=None):
        self.status_code = status_code
        self.detail = {
            "code": NOT_LOGIN_CODE,
            "message": f"{name} 未登录！"
        }


class LogoutResponse(HTTPException):
    def __init__(self, status_code=status.HTTP_200_OK, name=None, patt=None):
        self.status_code = status_code
        self.detail = {
            "code": LOGOUT_CODE,
            "message": f"{name} 退出登录成功！"
        }
