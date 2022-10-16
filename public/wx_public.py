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
from zhdate import ZhDate
from requests_html import HTMLSession

from public.log import logger
from conf.settings import TOKEN, FOLLOW
from public.shares import shares


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
        media_id = media_list[random.randint(0, len(media_list) - 1)
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
    logger.info(f"加密：{hashcode}，微信返回：{signature}")
    if hashcode == signature:
        return True


def age_content(date: list):
    """
    年龄相关
    :param date:
    :return:
    """
    year, mouth, day = date[0].split(".")
    age = datetime.date(int(year), int(mouth), int(day))
    age_date = datetime.datetime(int(year), int(mouth), int(day))
    lunar = ZhDate.from_datetime(age_date)
    now = datetime.datetime.now().date()
    age_num = str(now - age).split(" ")[0]
    age_50 = datetime.date(2043, 2, 9)
    age_60 = datetime.date(2053, 2, 9)
    age_70 = datetime.date(2063, 2, 9)
    age_80 = datetime.date(2073, 2, 9)
    age_100 = datetime.date(2093, 2, 9)
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


def send_wx_msg(rec_msg, token):
    content, media_id = "", ""
    if rec_msg.MsgType == 'text':
        logger.info(f"文本信息：{rec_msg.Content}")
        content = rec_msg.Content
        patt = r"[\d+]{4}.[\d+]{1,2}.[\d+]{1,2}"
        content = re.findall(patt, content)
        if content:
            content = age_content(content)
        else:
            if content in ["图片", "小七"] and token:
                media_id = wx_media(token)
            elif content in ["今天", "today"]:
                content = fishing(make=True)
            elif content == "放假":
                content = fishing()
            else:
                content = shares(stock_code=rec_msg.Content)
                if not content:
                    content = rec_msg.Content
    elif rec_msg.MsgType == 'event':
        content = FOLLOW
    elif rec_msg.MsgType == "image":
        if token:
            media_id = wx_media(token)
        else:
            media_id = rec_msg.MediaId
    logger.info(f"{content}===>>>{media_id}===>{token}")
    return content, media_id
