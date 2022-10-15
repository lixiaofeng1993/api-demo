#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: settings.py
# 说   明: 
# 创建时间: 2021/12/26 23:30
# @Version：V 0.1
# @desc :

import platform
import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TOKEN = "lixiaofeng"
# AppID = "wx99e27a845c7d8c52"
AppID = "wx22a47e233a076ba9"
# AppSecret = "fff1120327c7297e536c44979a6273d3"
AppSecret = "3690a316ca019b01ecc2434577680b70"

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# 线上环境 False / True
DEBUG = True if platform.system() == "Windows" else False

HOST = "http://127.0.0.1:8000" if platform.system() == "Windows" else "http://121.41.54.234"
ASSETS_PATH = os.path.join(BASE_PATH, "media")
