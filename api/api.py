#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/29 19:23
# @Author  : lixiaofeng
# @Site    : 
# @File    : api.py
# @Software: PyCharm

import re
import random
import datetime
import requests
import efinance as ef
import hashlib
from faker import Faker
from fastapi import Depends, APIRouter
from requests_html import HTMLSession
from fastapi.responses import StreamingResponse

from conf.settings import HOST, ASSETS_PATH, os, DEBUG
from public.custom_code import result
from public.log import logger

router = APIRouter()


@router.get("/", summary="摸鱼办")
def get_calendar():
    result["result"] = {
        "title": "【摸鱼办宣】",
        "today": {},
        "holiday": {},
    }
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
        "2": ["元旦", "NewYear"],
        "3": ["春节", "SpringFestival"],
        "4": ["清明节", "TombSweeping"],
        "5": ["劳动节", "LabourDay"],
        "6": ["端午节", "DragonBoat"],
        "7": ["中秋节", "AutumnFestival"],
        "8": ["国庆节", "NationalDay"],
    }
    today = {
        "1": "GregorianCalendarDate",
        "2": "LunarDate",
        "3": "Week",
        "4": "Constellations",
        "5": "Season",
        "6": "SolarTerm",
        "7": "Festivals",
        "8": "HeavenlyStemsAndEarthlyBranches",
        "9": "FiveElements",
        "10": "Suitable",
        "11": "Taboo",
    }
    data = dict()
    week_day = "星期日"
    now = str(datetime.datetime.now().date()).split("-")
    # now = ["2022", "07", "25"]
    with HTMLSession() as session:
        res = session.get(f"https://www.rili.com.cn/wannianli/{now[0]}/{now[1]}{now[2]}.html").html
    for key, value in today.items():
        result["result"]["today"][value] = res.xpath(f'//div[@id="textbody"]/p/table/tr[{key}]/td[2]', first=True).text
        week_day = res.xpath('//div[@id="textbody"]/p/table/tr[3]/td[2]', first=True).text
    if week[week_day]:
        result["result"]["holiday"]["Weekend"] = f"还有 {week[week_day]} 天"
    else:
        result["result"]["holiday"]["Weekend"] = "当前是周末，要好好享受生活丫~"

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
        data[value[1]].update({
            "节日": value[0],
            "放假时间": day,
            "调休上班时间": work_day,
            "放假天数": days + "天",
        })
        _month, _day = re.findall(patt, day)[0]
        _month = int(_month) if _month.isdigit() else 1
        _day = int(_day) if _day.isdigit() else 1
        _time = datetime.date(now_year, _month, _day)
        diff_year = str(_time - now).split(" ")[0]
        if diff_year == "0:00:00":
            data[value[1]]["描述"] = f"今天是第一天！"
        elif abs(int(diff_year)) < int(days) - 1:
            data[value[1]]["描述"] = f"今天是第 {abs(int(diff_year)) + 1} 天！"
        elif abs(int(diff_year)) == int(days) - 1:
            data[value[1]]["描述"] = f"今天是最后一天……"
        elif "-" in diff_year:
            data[value[1]]["描述"] = f"距今天已过 {abs(int(diff_year))} 天 ^-^"
        else:
            data[value[1]]["描述"] = f"距今天还要 {diff_year} 天 ^-^"
    result["result"]["holiday"] = data
    return result


@router.get("/v1", summary="万年历api接口")
def get_calendar_api():
    week = {
        "星期一": 5,
        "星期二": 4,
        "星期三": 3,
        "星期四": 2,
        "星期五": 1,
        "星期六": 0,
        "星期日": 0,

    }
    now = str(datetime.datetime.now().date()).split("-")
    date = str(int(now[0])) + "-" + str(int(now[1])) + "-" + str(int(now[2]))
    res = requests.get(f"http://v.juhe.cn/calendar/day?date={date}&key=197557d5fc1f3a26fa772bc694ea4c2d").json()
    result = {
        "公告": "【摸鱼办宣】",
        "今天": {}
    }
    if res["reason"] == "Success" and res["error_code"] == 0:
        week_day = res["result"]["data"]["weekday"]
        if week[week_day]:
            result["今天"]["周　　末"] = f"还有 {week[week_day]} 天"
        else:
            result["今天"]["周　　末"] = "当前是周末，要好好享受生活丫~"
        result["今天"]["节　　日"] = res["result"]["data"]["holiday"]
        result["今天"]["假日描述"] = res["result"]["data"]["desc"]
        result["今天"]["公历日期"] = res["result"]["data"]["date"]
        result["今天"]["农历日期"] = res["result"]["data"]["lunar"]
        result["今天"]["年　　月"] = res["result"]["data"]["year-month"]
        result["今天"]["星　　期"] = week_day
        result["今天"]["纪　　年"] = res["result"]["data"]["lunarYear"]
        result["今天"]["属　　相"] = res["result"]["data"]["animalsYear"]
        result["今天"]["今日所宜"] = res["result"]["data"]["suit"]
        result["今天"]["今日所忌"] = res["result"]["data"]["avoid"]
    elif res["error_code"] == 10012:
        result["今天"] = "请求用完了，明天再来吧~"
    return result


@router.get("/age", summary="走过了多少天")
def get_calendar_api():
    age = datetime.date(1993, 2, 9)
    now = datetime.datetime.now().date()
    age_num = str(now - age).split(" ")[0]
    age_50 = datetime.date(2043, 2, 9)
    age_60 = datetime.date(2053, 2, 9)
    age_70 = datetime.date(2063, 2, 9)
    age_80 = datetime.date(2073, 2, 9)
    age_100 = datetime.date(2093, 2, 9)
    data = {
        "title": "走过了多少天",
        "born_in": "癸酉年正月十八",
        "pass_by": f" {age_num} 天",
        "so": {
            "fifty": f"到 半百 一共 {str(age_50 - age).split(' ')[0]} 天， 还剩下 {str(age_50 - now).split(' ')[0]} 天。",
            "sixty": f"到 花甲 一共 {str(age_60 - age).split(' ')[0]} 天， 还剩下 {str(age_60 - now).split(' ')[0]} 天。",
            "seventy": f"到 古稀 一共 {str(age_70 - age).split(' ')[0]} 天， 还剩下 {str(age_70 - now).split(' ')[0]} 天。",
            "eighty": f"到 耄耋 一共 {str(age_80 - age).split(' ')[0]} 天， 还剩下 {str(age_80 - now).split(' ')[0]} 天。",
            "hundred": f"到 期颐 一共 {str(age_100 - age).split(' ')[0]} 天， 还剩下 {str(age_100 - now).split(' ')[0]} 天。",
        }
    }
    result["result"] = data
    return result


@router.get("/girl/url", summary="获取美女图片地址")
async def get_girl():
    girl_list = os.listdir(ASSETS_PATH)
    girl = girl_list[random.randint(0, len(girl_list) - 1)]
    return {
        "code": 200,
        "img": f"{HOST}/media/{girl}" if DEBUG else f"{HOST}/{girl}"
    }


@router.get("/girl", summary="获取美女图片")
async def get_girl():
    girl_list = os.listdir(ASSETS_PATH)
    girl_path = os.path.join(ASSETS_PATH, girl_list[random.randint(0, len(girl_list) - 1)])
    girl = open(girl_path, mode="rb")
    return StreamingResponse(girl, media_type="image/jpg")


@router.get("/faker", summary="返回随机人物数据")
async def get_faker(number: int = 1):
    faker = Faker("zh-CN")
    number = 1 if number < 1 else number
    data = faker.profile()
    if number == 1:
        data["phone"] = faker.phone_number()
        data["card"] = faker.credit_card_number()
    else:
        del data["job"]
        del data["residence"]
        del data["current_location"]
        del data["website"]
        data["phone"] = []
        data["card"] = []
        data["ssn"] = []
        data["address"] = []
        data["mail"] = []
        for i in range(number):
            data["phone"].append(faker.phone_number())
            data["card"].append(faker.credit_card_number())
            data["address"].append(faker.address())
            data["ssn"].append(faker.ssn())
            data["mail"].append(faker.email())
    result["result"] = data
    return result


@router.get("/shares", summary="股票实时信息")
async def shares(stock_code: str = ""):
    # 股票代码
    stock_code = stock_code if stock_code else ["601069"]
    try:
        if isinstance(stock_code, str):
            stock_code = eval(stock_code)
    except:
        result["result"] = "参数类型错误！！！"
        return result
    # 数据间隔时间为 1 分钟
    freq = 1
    # 获取最新一个交易日的分钟级别股票行情数据
    df = ef.stock.get_quote_history(
        stock_code, klt=freq)
    data = list()
    for d in df:
        share_name = df[d]["股票名称"].values[0]
        open_price = df[d]["开盘"].values[0]
        new_price = df[d]["收盘"].values[-1]
        top_price = df[d]["最高"].max()
        down_price = df[d]["最低"].min()
        turnover = df[d]["成交量"].sum()
        average = df[d]["开盘"].mean()
        rise_and_fall = df[d]["涨跌幅"].sum()
        rise_and_price = df[d]["涨跌额"].sum()
        turnover_rate = df[d]["换手率"].sum()
        data.append({
            "股票名称": f"【{share_name}】",
            "开盘价": f" {open_price} 元/股",
            "最高价": f" {top_price} 元/股",
            "最低价": f" {down_price} 元/股",
            "平均价": f" {round(average, 2)} 元/股",
            "涨跌幅": f" {round(rise_and_fall, 2)} %",
            "涨跌额": f" {round(rise_and_price, 2)} 元",
            "成交量": f" {turnover} 手",
            "换手率": f" {round(turnover_rate, 2)} %",
            "最新价": f"【{new_price}】 元/股",
        })
    result["result"] = data
    return result


@router.get("/wx", summary="微信服务器配置验证")
async def handle_wx(signature, timestamp, nonce, echostr):
    try:
        token = "lixiaofeng"
        temp = [token, timestamp, nonce]
        temp.sort()
        hashcode = hashlib.sha1("".join(temp).encode('utf-8')).hexdigest()
        logger.info(f"加密：{hashcode}，微信返回：{signature}")
        logger.info(f"加密：{type(hashcode)}，微信返回：{type(signature)}")
        if hashcode == signature:
            logger.info(f"加1111111111111111密：{type(hashcode)}，微信返回：{type(signature)}")
            return echostr
        else:
            logger.info(f"222222222222222222222：{type(hashcode)}，微信返回：{type(signature)}")
            result["result"] = {"error": "验证失败！"}
            return result
    except Exception as error:
        logger.info(f"333333333333333333333333")
        result["result"] = {"error": error}
        return result
