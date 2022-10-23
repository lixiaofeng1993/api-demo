#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: wx_public.py
# 创建时间: 2022/10/15 0015 19:43
# @Version：V 0.1
# @desc :
import requests
import random
import hashlib

from jsonpath import jsonpath
from fastapi import Request
from sqlalchemy.orm import Session

from sql_app import crud_poetry
from public.recommend import recommend_handle, surplus_second, idiom_solitaire, idiom_info
from conf.settings import TOKEN, FOLLOW, ArticleUrl, DYNASTY, POETRY_TYPE
from public.shares import shares
from public.log import logger


def wx_media(token: str):
    """
    返回素材media_id
    :param token:
    :return:
    """
    url = f"https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token={token}"
    body = {
        "type": "image",
        "offset": 0,
        "count": 100
    }
    try:
        res = requests.post(url=url, json=body).json()
        media_list = jsonpath(res, "$.item[*].media_id")
        media_id = media_list[random.randint(0, len(media_list) - 1)]
        logger.info(f"media_id: {media_id}")
    except Exception as error:
        logger.error(f"获取media_id出现异常：{error}")
        return
    return media_id


def sign_sha1(signature, timestamp, nonce):
    """
    服务器配置 验证
    :param signature:
    :param timestamp:
    :param nonce:
    :return:
    """
    temp = [TOKEN, timestamp, nonce]
    temp.sort()
    hashcode = hashlib.sha1("".join(temp).encode('utf-8')).hexdigest()
    # logger.info(f"加密：{hashcode}，微信返回：{signature}")
    if hashcode == signature:
        return True


def handle_wx_text(data_list: list):
    content = ""
    for data in data_list:
        content += f"<a href='weixin://bizmsgmenu?msgmenucontent={data.id}&msgmenuid=9528'>{data.name}</a>\n"
    return content


def poetry_by_author_id(db: Session, request: Request, author_id: str, skip: int, flag: bool = False):
    """
    诗人对应诗词 更多
    """
    content = ""
    if flag:
        author = crud_poetry.get_author_by_id(db, author_id)
        content = author.dynasty.strip("\n") + author.name
    data_list = crud_poetry.get_poetry_by_author_id(db, author_id, skip=skip)
    if data_list:
        content += "\n诗词推荐：\n"
        content += handle_wx_text(data_list)
        content += ">>> 点击古诗名字 "
        more_text = f"<a href='weixin://bizmsgmenu?msgmenucontent=AUTHOR-{author_id}&msgmenuid=9527'>更多</a>"
        content += "或者查看 " + more_text if len(data_list) == 5 else ""
        request.app.state.redis.setex(key=f"AUTHOR-{author_id}", value=str(skip), seconds=30 * 60)
    return content


def poetry_by_type(db: Session, request: Request, text: str, skip: int, val):
    """
    古诗类型 更多
    """
    content = f"古诗类型：{text}\n古诗名字：\n"
    data_list = crud_poetry.get_poetry_by_type(db, text, skip=skip)
    content += handle_wx_text(data_list)
    content += ">>> 点击古诗名字 "
    more_text = f"<a href='weixin://bizmsgmenu?msgmenucontent=POETRY_TYPE-{val}&msgmenuid=9529'>更多</a> "
    content += "或者查看 " + more_text if len(data_list) == 10 else ""
    request.app.state.redis.setex(key=f"POETRY_TYPE-{val}", value=str(skip), seconds=30 * 60)
    return content


def author_by_dynasty(db: Session, request: Request, text: str, skip: int, val):
    """
    诗人朝代 更多
    """
    content = f"朝代：{text}\n诗人：\n"
    data_list = crud_poetry.get_author_by_dynasty(db, text, skip=skip)
    content += handle_wx_text(data_list)
    content += ">>> 点击诗人名字 "
    more_text = f"<a href='weixin://bizmsgmenu?msgmenucontent=DYNASTY-{val}&msgmenuid=9526'>更多</a> "
    content += "或者查看 " + more_text if len(data_list) == 10 else ""
    request.app.state.redis.setex(key=f"DYNASTY-{val}", value=str(skip), seconds=30 * 60)
    return content


def send_author(db: Session, request: Request, data):
    """
    输入作者，返回作者简介及古诗词推荐
    """
    content = ""
    if data.dynasty:
        content += data.dynasty.strip("\n") + data.name
    if data.introduce:
        introduce = data.introduce.split("►")[0] if "►" in data.introduce else data.introduce
        content += "\n介绍：\n" + introduce.strip("\n")
    content += poetry_by_author_id(db, request, data.id, skip=0)
    return content


def send_poetry(data):
    """
    输入古诗词名称，返回名句、赏析等数据
    """
    content = f"《{data.name}》\n类型：{data.type}"
    if data.phrase:
        content += "\n名句：\n" + data.phrase.strip("\n")
    if data.explain:
        content += "\n赏析：\n" + data.explain.strip("\n")
    if data.original:
        content += "\n原文：\n" + data.original.strip("\n")
    if data.translation:
        content += "\n译文：\n" + data.translation.strip("\n")
    if data.background:
        content += "\n创作背景：\n" + data.background.strip("\n")
    return content


def send_more(db: Session, request: Request, text: str, skip: str, content: str = ""):
    if "DYNASTY-" in text or "POETRY_TYPE-" in text or "AUTHOR-" in text or "RECOMMEND-" in text:
        skip = int(skip) if skip.isdigit() else skip
        val = text.split("-")[-1]
        if "RECOMMEND" in text:
            data = crud_poetry.get_poetry_by_id(db, val)
            if data.original:
                content += "原文：\n" + data.original.strip("\n")
            if data.translation:
                content += "\n译文：\n" + data.translation.strip("\n")
            if data.background:
                content += "\n创作背景：\n" + data.background.strip("\n")
        elif "DYNASTY" in text:
            for key, value in DYNASTY.items():
                if int(val) == value:
                    text = key
            content = author_by_dynasty(db, request, text, skip + 10, val)
        elif "POETRY_TYPE" in text:
            for key, value in POETRY_TYPE.items():
                if int(val) == value:
                    text = key
            content = poetry_by_type(db, request, text, skip + 10, val)
        elif "AUTHOR" in text:
            content = poetry_by_author_id(db, request, val, skip=skip + 5, flag=True)
    return content


def poetry_content(db: Session, request: Request, text: str, skip: str = "0"):
    content = ""
    if skip:
        content = send_more(db, request, text, skip)
        return content
    elif len(text) == 32:
        author = crud_poetry.get_author_by_id(db, text)
        if author:
            content = send_author(db, request, author)
            return content
        else:
            poetry = crud_poetry.get_poetry_by_id(db, text)
            if poetry:
                content = send_poetry(poetry)
                return content
    else:
        if text == "推荐":
            poetry_type = recommend_handle()  # 根据季节、天气返回古诗词类型
            poetry = crud_poetry.get_poetry_by_type_random(db, poetry_type)
            phrase = poetry.phrase.strip('\n')
            explain = poetry.explain.strip('\n')
            if poetry.author_id:
                content = f"今天推荐：\n出自{poetry.author.dynasty}{poetry.author.name}的《{poetry.name}》" \
                          f"\n类型：{poetry_type}\n\n{phrase}\n"
            else:
                content = f"今天推荐：\n摘自《{poetry.name}》\n类型：{poetry_type}\n\n{phrase}\n"
            if poetry.explain:
                content += f"\n赏析：\n{explain}"
            content += "\n>>> 点击查看 " \
                       f"<a href='weixin://bizmsgmenu?msgmenucontent=RECOMMEND-{poetry.id}&msgmenuid=9525'>更多</a>"
            seconds = surplus_second()  # 返回今天剩余秒数
            request.app.state.redis.setex(key=f"RECOMMEND-{poetry.id}", value=poetry.id, seconds=seconds)  # 更多缓存
            request.app.state.redis.setex(key=f"recommended-today", value=content, seconds=seconds)  # 推荐缓存
            return content
        for key, value in DYNASTY.items():  # 诗人朝代
            if text == key:
                content = author_by_dynasty(db, request, text, 0, value)
                return content
        for key, value in POETRY_TYPE.items():  # 古诗词类型
            if text == key:
                content = poetry_by_type(db, request, text, 0, value)
                return content
        data = crud_poetry.get_author_by_name(db, text)  # 诗人名称
        if data:
            content = send_author(db, request, data)
        else:
            data = crud_poetry.get_poetry_by_name(db, text)  # 古诗名称
            if data:
                content = send_poetry(data)
            else:
                data = crud_poetry.get_poetry_by_phrase(db, text)  # 古诗名句
                if data:
                    content = f"古诗名字：\n" + f"<a href='weixin://bizmsgmenu?msgmenucontent={data.id}&msgmenuid=9524'>" \
                                           f"{data.name}</a>"
    return content


def send_wx_msg(db: Session, request: Request, rec_msg, token: str, skip: str, idiom: str = ""):
    """
    :param db:
    :param request:
    :param rec_msg: 微信返回文案
    :param token: 微信登录token
    :param skip: 更多跳转页数
    :param idiom: 成语接龙
    :return 回复文案和图片id
    """
    content, media_id = "", ""
    if rec_msg.MsgType == 'text':
        text = rec_msg.Content
        logger.info(f"文本信息：{text}")
        if idiom:
            if "#INFO#" in text:
                idiom_name = text.split("-")[0]
                content = idiom_info(idiom_name)
            else:
                content = idiom_solitaire(text)
        else:
            content = poetry_content(db, request, text, skip)  # 古诗词返回判断
        if not content:
            if text in ["图片", "小七"] and token:
                media_id = wx_media(token)
            elif text in ["all", "文章"]:
                content = ArticleUrl
            elif text in ["follow", "功能"]:
                content = FOLLOW
            else:
                content = shares(stock_code=text)
                if not content:
                    content = text
    elif rec_msg.MsgType == 'event':
        if rec_msg.Event == "subscribe":
            content = FOLLOW
        elif rec_msg.Event == "unsubscribe":
            logger.info(f"用户 {rec_msg.FromUserName} 取消关注了！！！")
    elif rec_msg.MsgType == "image":
        if token:
            media_id = wx_media(token)
        else:
            media_id = rec_msg.MediaId
    return content, media_id
