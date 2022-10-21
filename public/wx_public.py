#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
# 创 建 人: 李先生
# 文 件 名: wx_public.py
# 创建时间: 2022/10/15 0015 19:43
# 版   本：V 0.1
# 说   明: 
"""

import requests
import random
import hashlib
import aiohttp
import datetime
import re

from jsonpath import jsonpath
from fastapi import Request
from sqlalchemy.orm import Session
from zhdate import ZhDate
from requests_html import HTMLSession

from sql_app import crud_poetry
from public.recommend import recommend_handle
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


def age_content(date: list):
    """
    年龄相关
    :param date:
    :return:
    """
    year, mouth, day = date[0].split(".")
    year, mouth, day = int(year), int(mouth), int(day)
    age = datetime.date(year, mouth, day)
    age_date = datetime.datetime(year, mouth, day)
    lunar = ZhDate.from_datetime(age_date)
    now = datetime.datetime.now().date()
    age_num = str(now - age).split(" ")[0]
    age_50 = datetime.date(year + 50, 2, 9)
    age_60 = datetime.date(year + 60, 2, 9)
    age_70 = datetime.date(year + 70, 2, 9)
    age_80 = datetime.date(year + 80, 2, 9)
    age_100 = datetime.date(year + 100, 2, 9)
    data = f"阴历：{lunar.chinese()}\n距今天过去了 {age_num} 天\n然后呢：\n到 半百 一共 {str(age_50 - age).split(' ')[0]}" \
           f" 天，还剩 {str(age_50 - now).split(' ')[0]} 天\n到 花甲 一共 {str(age_60 - age).split(' ')[0]} 天， " \
           f"还剩下 {str(age_60 - now).split(' ')[0]} 天\n到 古稀 一共 {str(age_70 - age).split(' ')[0]} 天， 还剩下 " \
           f"{str(age_70 - now).split(' ')[0]} 天\n到 耄耋 一共 {str(age_80 - age).split(' ')[0]} 天， 还剩下 " \
           f"{str(age_80 - now).split(' ')[0]} 天\n到 期颐 一共 {str(age_100 - age).split(' ')[0]} 天， 还剩下 " \
           f"{str(age_100 - now).split(' ')[0]} 天"
    return data


def fishing(make=False):
    week = {
        "星期一": 5,
        "星期二": 4,
        "星期三": 3,
        "星期四": 2,
        "星期五": 1,
        "星期六": 0,
        "星期日": 0,

    }
    holiday = {
        "2": "元旦：",
        "3": "春节：",
        "4": "清明节：",
        "5": "劳动节：",
        "6": "端午节：",
        "7": "中秋节：",
        "8": "国庆节：",
    }
    today = {
        "1": "公历日期：",
        "2": "农历日期：",
        "3": "星　　期：",
        "4": "星　　座：",
        "5": "季　　节：",
        "6": "节　　气：",
        "7": "节　　日：",
        "8": "天干地支：",
        "9": "五　　行：",
        "10": "今日所宜：",
        "11": "今日所忌：",
    }
    data = dict()
    week_day = "星期日"
    today_content, content = "", ""
    now = str(datetime.datetime.now().date()).split("-")
    # now = ["2022", "07", "25"]
    with HTMLSession() as session:
        res = session.get(f"https://www.rili.com.cn/wannianli/{now[0]}/{now[1]}{now[2]}.html").html
    for key, value in today.items():
        today_content += value + res.xpath(f'//div[@id="textbody"]/p/table/tr[{key}]/td[2]', first=True).text + "\n"
        week_day = res.xpath('//div[@id="textbody"]/p/table/tr[3]/td[2]', first=True).text
    if week[week_day]:
        content += f"距周末还有 {week[week_day]} 天" + "\n"
    else:
        content += "当前是周末，要好好享受生活丫~" + "\n"

    with HTMLSession() as session:
        now = datetime.datetime.now().date()
        res = session.get("https://www.rili.com.cn/fangjiaanpai/").html
    now_year_num = res.find("#fjb_title")[0].text[2:6]
    now_year = int(now_year_num) if now_year_num.isdigit() else 2022
    patt = r"(\d{1,2})月(\d{1,2})日~"
    for key, value in holiday.items():
        data[value[1]] = dict()
        day = res.xpath(f'//*[@id="fjb_id"]/tr[{key}]/td[2]')[0].text
        work_day = res.xpath(f'//*[@id="fjb_id"]/tr[{key}]/td[3]')[0].text
        days = res.xpath(f'//*[@id="fjb_id"]/tr[{key}]/td[4]')[0].text[:1]
        content += value + "\n" + "放假时间：" + day + "\n" + "调休上班时间：" + work_day + "\n" + "放假天数：" + days + "天\n"
        _month, _day = re.findall(patt, day)[0]
        _month = int(_month) if _month.isdigit() else 1
        _day = int(_day) if _day.isdigit() else 1
        _time = datetime.date(now_year, _month, _day)
        diff_year = str(_time - now).split(" ")[0]
        if diff_year == "0:00:00":
            content += f"今天是第一天！" + "\n"
        elif abs(int(diff_year)) < int(days) - 1:
            content += f"今天是第 {abs(int(diff_year)) + 1} 天！" + "\n"
        elif abs(int(diff_year)) == int(days) - 1:
            content += f"今天是最后一天……" + "\n"
        elif "-" in diff_year:
            content += f"距今天已过 {abs(int(diff_year))} 天 ^-^" + "\n"
        else:
            content += f"距今天还要 {diff_year} 天 ^-^" + "\n"
    if make:
        return today_content
    return content


def handle_wx_text(data_list: list):
    content = ""
    for data in data_list:
        content += f"<a href='weixin://bizmsgmenu?msgmenucontent={data.id}&msgmenuid={data.name}'>{data.name}</a>\n"
    return content


def send_author(db: Session, request: Request, data):
    """
    输入作者，返回作者简介及古诗词推荐
    """
    content = data.name
    introduce = data.introduce.split("►")[0] if "►" in data.introduce else data.introduce
    if data.dynasty:
        content += "\n朝代：" + data.dynasty.strip("\n")
    if introduce:
        content += "\n介绍：\n" + introduce.strip("\n")
    data_list = crud_poetry.get_poetry_by_author_id(db, data.id)
    if data_list:
        content += "\n诗词推荐：\n"
        content += handle_wx_text(data_list)
        content += ">>> 点击古诗名字 "
        more_text = f" <a href='weixin://bizmsgmenu?msgmenucontent=AUTHOR-{data.id}&msgmenuid=POETRY_TYPE-{data.id}'>更多</a> "
        content += "或者查看" + more_text if len(data_list) == 10 else ""
        request.app.state.redis.setex(key=f"AUTHOR-{data.id}", value="0", seconds=30 * 60)
    return content


def send_poetry(data, content: str = ""):
    """
    输入古诗词名称，返回名句、赏析等数据
    """
    if data.phrase:
        content += "名句：\n" + data.phrase.strip("\n")
    if data.explain:
        content += "\n赏析：\n" + data.explain.strip("\n")
    if data.original:
        content += "\n原文：\n" + data.original.strip("\n")
    if data.translation:
        content += "\n译文：\n" + data.translation.strip("\n")
    if data.background:
        content += "\n创作背景：\n" + data.background.strip("\n")
    return content


def send_more(db: Session, request: Request, text: str, skip: str, content=""):
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
            data_list = crud_poetry.get_author_by_dynasty(db, text, skip=skip + 10)
            content = f"朝代：{text}\n诗人：\n"
            content += handle_wx_text(data_list)
            more_text = f" <a href='weixin://bizmsgmenu?msgmenucontent=DYNASTY-{val}&msgmenuid=DYNASTY-{val}'>更多</a> "
            content += ">>> 点击诗人名字 "
            content += "或者查看" + more_text if len(data_list) == 10 else ""
            request.app.state.redis.setex(key=f"DYNASTY-{val}", value=str(skip + 10), seconds=30 * 60)
        elif "POETRY_TYPE" in text:
            for key, value in POETRY_TYPE.items():
                if int(val) == value:
                    text = key
            data_list = crud_poetry.get_poetry_by_type(db, text, skip=skip + 10)
            content = f"古诗类型：{text}\n古诗名字：\n"
            content += handle_wx_text(data_list)
            content += ">>> 点击古诗名字 "
            more_text = f" <a href='weixin://bizmsgmenu?msgmenucontent=POETRY_TYPE-{val}&msgmenuid=POETRY_TYPE-{val}'>更多</a> "
            content += "或者查看" + more_text if len(data_list) == 10 else ""
            request.app.state.redis.setex(key=f"POETRY_TYPE-{val}", value=str(skip + 10), seconds=30 * 60)
        elif "AUTHOR" in text:
            data_list = crud_poetry.get_poetry_by_author_id(db, val, skip=skip + 10)
            content += "诗词推荐：\n"
            content += handle_wx_text(data_list)
            content += ">>> 点击古诗名字 "
            more_text = f" <a href='weixin://bizmsgmenu?msgmenucontent=AUTHOR-{val}&msgmenuid=POETRY_TYPE-{val}'>更多</a> "
            content += "或者查看" + more_text if len(data_list) == 10 else ""
            request.app.state.redis.setex(key=f"AUTHOR-{val}", value=str(skip + 10), seconds=30 * 60)
    return content


def poetry_content(db: Session, request: Request, text: str, skip: str = "0"):
    content = ""
    if skip:
        content = send_more(db, request, text, skip)
    elif len(text) == 32:
        author = crud_poetry.get_author_by_id(db, text)
        if author:
            content = send_author(db, request, author)
            return content
        else:
            poetry = crud_poetry.get_poetry_by_id(db, text)
            if poetry:
                content = send_poetry(poetry, "")
                return content
    else:
        if text == "推荐":
            poetry_type = recommend_handle()
            poetry = crud_poetry.get_poetry_by_type_random(db, poetry_type)
            phrase = poetry.phrase.strip('\n')
            explain = poetry.explain.strip('\n')
            request.app.state.redis.setex(key=f"RECOMMEND-{poetry.id}", value=poetry.id, seconds=30 * 60)
            if poetry.author_id:
                content = f"今天推荐：\n出自{poetry.author.dynasty}{poetry.author.name}的《{poetry.name}》\n\n{phrase}\n"
            else:
                content = f"今天推荐：\n摘自《{poetry.name}》\n\n{phrase}\n"
            if poetry.explain:
                content += f"\n赏析：\n{explain}"
            content += "\n>>>点击查看 " \
                       f"<a href='weixin://bizmsgmenu?msgmenucontent=RECOMMEND-{poetry.id}&msgmenuid=RECOMMEND-{poetry.id}'>更多</a>"
            return content
        for key, value in DYNASTY.items():
            if text == key:
                request.app.state.redis.setex(key=f"DYNASTY-{value}", value="0", seconds=30 * 60)
                data_list = crud_poetry.get_author_by_dynasty(db, text)
                content = f"朝代：{text}\n诗人：\n"
                content += handle_wx_text(data_list)
                content += ">>> 点击诗人名字 "
                more_text = f" <a href='weixin://bizmsgmenu?msgmenucontent=DYNASTY-{value}&msgmenuid=DYNASTY-{value}'>更多</a> "
                content += "或者查看" + more_text if len(data_list) == 10 else ""
                return content
        for key, value in POETRY_TYPE.items():
            if text == key:
                request.app.state.redis.setex(key=f"POETRY_TYPE-{value}", value="0", seconds=30 * 60)
                data_list = crud_poetry.get_poetry_by_type(db, text)
                content = f"古诗类型：{text}\n古诗名字：\n"
                content += handle_wx_text(data_list)
                content += ">>> 点击古诗名字 "
                more_text = f" <a href='weixin://bizmsgmenu?msgmenucontent=POETRY_TYPE-{value}&msgmenuid=POETRY_TYPE-{value}'>更多</a> "
                content += "或者查看" + more_text if len(data_list) == 10 else ""
                return content
        data = crud_poetry.get_author_by_name(db, text)
        if data:
            content = send_author(db, request, data)
        else:
            data = crud_poetry.get_poetry_by_name(db, text)
            if data:
                content = send_poetry(data, "")
            else:
                data = crud_poetry.get_poetry_by_phrase(db, text)
                if data:
                    content = f"古诗名字：\n" + f"<a href='weixin://bizmsgmenu?msgmenucontent={data.id}&" \
                                           f"msgmenuid={data.id}'>{data.name}</a>\n>>> 点击古诗名字获取更多..."
    return content


def send_wx_msg(db: Session, request: Request, rec_msg, token: str, skip: str):
    content, media_id = "", ""
    if rec_msg.MsgType == 'text':
        text = rec_msg.Content
        logger.info(f"文本信息：{text}")
        content = poetry_content(db, request, text, skip)
        if not content:
            if text in ["图片", "小七"] and token:
                media_id = wx_media(token)
            elif text in ["all", "文章"]:
                content = ArticleUrl
            elif text in ["follow", "功能"]:
                content = FOLLOW
            elif text in ["今天", "today"]:
                content = fishing(make=True)
            elif text == "放假":
                content = fishing()
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
