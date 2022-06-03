#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: custom_code.py
# 说   明: 
# 创建时间: 2022/2/11 12:37
# @Version：V 0.1
# @desc :

# 返回成功
result = {"code": 200, "message": "请求成功", "result": ""}
# 请求异常
response_error = {400: {"message": "请求异常！"}}

# token校验失败
EXCEPTION_TOKEN_CODE = 10000
# 非活跃用户
EXCEPTION_ACTIVE_CODE = 10001
# 已登录
EXCEPTION_LOGIN_CODE = 10002
# 密码错误
EXCEPTION_PASS_CODE = 10003
# 登录用户没有权限
EXCEPTION_SUPER_CODE = 10004
# 删除失败
EXCEPTION_DELETE_CODE = 10005
# 不存在
EXCEPTION_NOT_EXIT_CODE = 10006
# 已存在
EXCEPTION_ALREADY_EXIST_CODE = 10007
# 不符合格式
EXCEPTION_FORMAT_CODE = 10008
# 检查错误
EXCEPTION_CHECK_CODE = 10009
# 退出登录
LOGOUT_CODE = 10010
# 未登录
NOT_LOGIN_CODE = 10011
