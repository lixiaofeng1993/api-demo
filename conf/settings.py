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

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# 线上环境 False / True
DEBUG = True if platform.system() == "Windows" else False

HOST = "http://127.0.0.1:8000" if platform.system() == "Windows" else "http://121.41.54.234"
ASSETS_PATH = os.path.join(BASE_PATH, "media")

# 微信公众号
TOKEN = "lixiaofeng"
AppID = "wx99e27a845c7d8c52"
AppSecret = "fff1120327c7297e536c44979a6273d3"

FOLLOW = "这世界怎么那么多人，蹉跎回首，已不再年轻。\n这世界怎么那么多人，兜兜转转，浑噩半生。\n这世界怎么那么多人......" \
         "回复 日期格式 xxxx.xx.xx <示例 【1993.05.16】>，返回已经走过的天数信息\n" \
         "回复 【图片】 or 【小七】，返回小七美照\n" \
         "回复 【今天】 or 【today】，返回万年历当天信息\n" \
         "回复 【放假】，返回万年历当年放假安排\n" \
         "回复 【股票名称或者股票代码】，返回当天股票走势信息\n"
