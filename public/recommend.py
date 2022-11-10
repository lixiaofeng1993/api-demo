#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: recommend.py
# 创建时间: 2022/10/14 0014 21:52
# @Version：V 0.1
# @desc :
import requests
import time
from datetime import date
from jsonpath import jsonpath
from random import randint

from conf.settings import GAO_KEY, CITY_CODE, IDIOM_KEY, IDIOM_INFO, CALENDAR_KEY, POETRY_TYPE, WEATHER_KEY, CITY_NAME
from public.log import logger


def get_holiday():
    now = date.today()
    day = str(int(now.year)) + "-" + str(int(now.month)) + "-" + str(int(now.day))
    res = requests.get(f"http://v.juhe.cn/calendar/day?date={day}&key={CALENDAR_KEY}").json()
    if res["error_code"] == 10012:
        logger.error(f"获取当天的详细信息接口 请求超过次数限制 ===>>> {res['reason']} ===>>> {res['error_code']}")
        return
    elif res["error_code"] != 0:
        logger.error(f"获取当天的详细信息接口出现异常 ===>>> {res['reason']} ===>>> {res['error_code']}")
        return
    holiday = res["result"]["data"]["holiday"]
    return holiday


def get_weather():
    # params = {
    #     "key": f"{GAO_KEY}",
    #     "city": f"{CITY_CODE}",
    #     "extensions": "base",
    #     "output": "JSON",
    # }
    # res = requests.get("https://restapi.amap.com/v3/weather/weatherInfo", params=params, verify=False)
    # res.encoding = "utf-8"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {
        "key": WEATHER_KEY,
        "city": CITY_NAME
    }
    res = requests.get("http://apis.juhe.cn/simpleWeather/query", headers=headers, params=params, verify=False).json()
    if res["error_code"] == 10012:
        logger.error(f"根据城市查询天气接口 请求超过次数限制 ===>>> {res['reason']} ===>>> {res['error_code']}")
        return
    elif res["error_code"] != 0:
        logger.error(f"根据城市查询天气接口出现异常 ===>>> {res['reason']} ===>>> {res['error_code']}")
        return
    weather = jsonpath(res, "$.result.realtime.info")
    return weather[0] if weather else ""


def now_season():
    """
    立春 2月3-5日
    立夏 5月05-07日
    立秋 8月7或8日
    立冬 11月7-8日
    """
    season = ""
    month = date.today().month
    day = date.today().day
    if month in [3, 4]:
        season = "春天"
    elif month in [6, 7]:
        season = "夏天"
    elif month in [9, 10]:
        season = "秋天"
    elif month in [12, 1]:
        season = "冬天"
    elif month == 2:
        if day in [3, 4, 5]:
            return "豪放"
        elif day < 3:
            return "冬天"
        elif day > 5:
            return "春天"
    elif month == 5:
        if day in [5, 6, 7]:
            return "豪放"
        elif day < 5:
            return "春天"
        elif day > 7:
            return "夏天"
    elif month in [8, 11]:
        if day in [7, 8]:
            return "豪放"
        elif day < 7:
            return "夏天" if month == 8 else "秋天"
        elif day > 8:
            return "秋天" if month == 8 else "冬天"
    return season


def recommend_handle():
    holiday = get_holiday()
    if holiday and holiday in POETRY_TYPE.keys():
        poetry_type = holiday
    else:
        weather = get_weather()
        type_list = list()
        if weather:
            if "晴" in weather:
                type_list = ["爱情", "友情"]
            elif "雨" in weather:
                type_list = ["写雨", "思乡", "离别", "伤感"]
            elif "风" in weather:
                type_list = ["写风"]
            elif "雪" in weather:
                type_list = ["写雪", "梅花"]
            elif "云" in weather:
                type_list = ["写云"]
            elif "沙" in weather or "霾" in weather:
                type_list = ["边塞"]
        type_list.append(now_season())
        poetry_type = type_list[randint(0, len(type_list) - 1)]
    return poetry_type


def surplus_second():
    today = date.today()
    today_end = f"{str(today)} 23:59:59"
    end_second = int(time.mktime(time.strptime(today_end, "%Y-%m-%d %H:%M:%S")))
    now_second = int(time.time())
    return end_second - now_second


def idiom_solitaire(text: str):
    url = "http://apis.juhe.cn/idiomJie/query"
    params = {
        "key": IDIOM_KEY,
        "wd": text,
        "size": 10,
        "is_rand": 1,  # 是否随机返回结果，1:是 2:否。默认2
    }
    res = requests.get(url, params=params, verify=False).json()
    if res["error_code"] == 10012:
        logger.error(f"成语接龙api ===>>> {res['reason']} ===>>> {res['error_code']}")
        content = "emmm，api每天只能请求50次，明天再来吧！"
        return content
    elif res["error_code"] != 0:
        logger.error(f"成语接龙api ===>>> {res['reason']} ===>>> {res['error_code']}")
        content = f"emmm，成语接龙出现异常了嘿，我跑着去看看因为啥 >>> {res['error_code']}"
        return content
    data_list = res["result"]["data"]
    last_word = res["result"]["last_word"]
    content = "成语接龙开始咯！\n"
    more_text = f"<a href='weixin://bizmsgmenu?msgmenucontent=IDIOM-INFO-{text}&msgmenuid={text}'>{text}</a>"
    if not data_list:
        content += f"emmm，结束了嘿，么有找到 {last_word} 开头的成语。\n了解更多点击 {more_text}"
        return content
    content += f'最后一个字：{last_word}\n'
    for data in res["result"]["data"]:
        content += f"<a href='weixin://bizmsgmenu?msgmenucontent={data}&msgmenuid=9523'>{data}</a>\n"
    content += f">>> 点击成语 或者查看 {more_text}"
    return content


def idiom_info(text: str):
    url = "http://apis.juhe.cn/idioms/query"
    params = {
        "key": IDIOM_INFO,
        "wd": text,
    }
    res = requests.get(url, params=params, verify=False).json()
    if res["error_code"] == 2015702:
        content = f"emmm，么有查询到 【{text}】 的信息，要不试试 #{text} ？"
        return content
    elif res["error_code"] == 10012:
        logger.error(f"成语大全api ===>>> {res['reason']} ===>>> {res['error_code']}")
        content = "emmm，api每天只能请求50次，明天再来吧！"
        return content
    elif res["error_code"] != 0:
        logger.error(f"成语大全api ===>>> {res['reason']} ===>>> {res['error_code']}")
        content = f"emmm，成语大全出现异常了嘿，我跑着去看看因为啥 >>> {res['error_code']}"
        return content
    name = res["result"]["name"]  # 成语
    pinyin = res["result"]["pinyin"]  # 拼音
    jbsy = res["result"]["jbsy"]  # 基本释义
    xxsy = res["result"]["xxsy"]  # 详细释义
    chuchu = res["result"]["chuchu"]  # 出处
    liju = res["result"]["liju"]  # 例句
    # jyc = res["result"]["jyc"]  # 近义词
    # fyc = res["result"]["fyc"]  # 反义词
    content = f"成语：{name}\n"
    if pinyin:
        content += f"拼音：{pinyin}\n"
    if xxsy:
        content += "详细释义：\n"
        for data in xxsy:
            content += data + "\n"
    else:
        if jbsy:
            content += "基本释义：\n"
            for data in jbsy:
                content += data + "\n"
        if chuchu:
            content += f"出处：\n{chuchu}\n"
        if liju:
            content += f"例句：\n{liju}"
    return content


if __name__ == '__main__':
    print(now_season())
