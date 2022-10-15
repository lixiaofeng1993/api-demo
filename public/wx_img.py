#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
# 创 建 人: 李先生
# 文 件 名: wx_img.py
# 创建时间: 2022/10/15 0015 19:43
# 版   本：V 0.1
# 说   明: 
"""

import requests
import random

from jsonpath import jsonpath


def wx_media(token: str):
    url = f"https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token={token}"
    body = {
        "type": "image",
        "offset": 0,
        "count": 100
    }

    res = requests.post(url=url, json=body).json()
    media_list = jsonpath(res, "$.item[*].media_id")
    media_id = media_list[random.randint(0, len(media_list) - 1)]
    return media_id
