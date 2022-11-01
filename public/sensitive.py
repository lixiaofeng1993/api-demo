#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: sensitive.py
# 创建时间: 2022/11/1 0001 18:34
# @Version：V 0.1
# @desc :
import requests
from public.log import logger


def sensitive_words(text: str = ""):
    data = {
        "content": text,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }
    url = "http://www.zhipaiwu.com/index.php/Weijinci/postIndex.html"
    res = requests.post(url, headers=headers, data=data, verify=False)
    try:
        response = res.json()
        if response["code"] == 200:
            msg_list = response["result"]["minganArr"]
            if isinstance(msg_list, list):
                logger.info(f"检测到的敏感词 ===>>> {msg_list}")
                for msg in msg_list:
                    text = text.replace(msg, "*" * len(msg))
    except Exception as error:
        logger.error(f"敏感词请求出现异常 ===>>> {error}")
    return text
