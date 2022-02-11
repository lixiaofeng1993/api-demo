#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: field_check.py
# 说   明: 
# 创建时间: 2021/12/28 18:57
# @Version：V 0.1
# @desc :
import re

from public import exception


def check_name(name: str) -> None:
    pattern = r"[A-Za-z1-9\-\_]{1,20}"
    patt = re.match(pattern, name)
    if not patt:
        raise exception.FormatFieldException(name=name, patt=pattern)


def check_zh_name(name: str) -> None:
    pattern = r"[^x00-xff]{1,20}"
    patt = re.match(pattern, name)
    if not patt:
        raise exception.FormatFieldException(name=name, patt=pattern)


def check_password(name: str) -> None:
    pattern = r"[A-Za-z1-9\-\_]{6,100}"
    patt = re.match(pattern, name)
    if not patt:
        raise exception.FormatFieldException(name=name, patt=pattern)


def check_email(name: str) -> None:
    pattern = r"(^[\w\.\-]+\@[\w\.\-]+\.[A-Za-z]{2,4}$){1,50}"
    patt = re.match(pattern, name)
    if not patt or len(name) > 50:
        raise exception.FormatFieldException(name=name, patt=pattern)
