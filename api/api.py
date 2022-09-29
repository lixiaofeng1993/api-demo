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
from faker import Faker
from fastapi import Depends, APIRouter
from requests_html import HTMLSession
from fastapi.responses import StreamingResponse

from conf.settings import HOST, ASSETS_PATH, os, DEBUG
from public.custom_code import result

router = APIRouter()


@router.get("/", summary="解析html数据")
def get_calendar():
    result["result"] = {
        "title": "摸鱼办宣",
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
    now = str(datetime.datetime.now().date()).split("-")
    # now = ["2022", "07", "25"]
    with HTMLSession() as session:
        res = session.get(f"https://www.rili.com.cn/wannianli/{now[0]}/{now[1]}{now[2]}.html").html
    result["result"]["today"]["gregorian"] = res.xpath('//div[@id="textbody"]/p/table/tr[1]/td[2]', first=True).text
    result["result"]["today"]["lunar"] = res.xpath('//div[@id="textbody"]/p/table/tr[2]/td[2]', first=True).text
    week_day = res.xpath('//div[@id="textbody"]/p/table/tr[3]/td[2]', first=True).text
    result["result"]["today"]["week"] = week_day
    result["result"]["today"]["constellations"] = res.xpath('//div[@id="textbody"]/p/table/tr[4]/td[2]',
                                                            first=True).text
    result["result"]["today"]["season"] = res.xpath('//div[@id="textbody"]/p/table/tr[5]/td[2]', first=True).text
    result["result"]["today"]["Solar"] = res.xpath('//div[@id="textbody"]/p/table/tr[6]/td[2]', first=True).text
    result["result"]["today"]["festivals"] = res.xpath('//div[@id="textbody"]/p/table/tr[7]/td[2]', first=True).text
    result["result"]["today"]["three_volts_count_nine"] = res.xpath('//div[@id="textbody"]/p/table/tr[8]/td[2]',
                                                                    first=True).text
    result["result"]["today"]["suitable"] = res.xpath('//div[@id="textbody"]/p/table/tr[11]/td[2]', first=True).text
    result["result"]["today"]["taboo"] = res.xpath('//div[@id="textbody"]/p/table/tr[12]/td[2]', first=True).text
    with HTMLSession() as session:
        now = datetime.datetime.now().date()
        res = session.get("https://www.rili.com.cn/fangjiaanpai/").html
    now_year_num = res.find("#fjb_title")[0].text[2:6]
    now_year = int(now_year_num) if now_year_num.isdigit() else 2022
    new_year_month_day = res.xpath('//*[@id="fjb_id"]/tr[2]/td[2]')[0].text
    patt = r"(\d{1,2})月(\d{1,2})日~"
    new_year_month, new_year_day = re.findall(patt, new_year_month_day)[0]
    new_year_month = int(new_year_month) if new_year_month.isdigit() else 1
    new_year_day = int(new_year_day) if new_year_day.isdigit() else 1
    new_year = datetime.date(now_year, new_year_month, new_year_day)
    diff_new_year = str(new_year - now).split(" ")[0]
    if week[week_day]:
        result["result"]["holiday"]["weekend"] = f"还有 {week[week_day]} 天"
    else:
        result["result"]["holiday"]["weekend"] = "当前是周末，要好好享受生活丫~"
    if "-" in diff_new_year:

        result["result"]["holiday"]["new_year_day"] = f"已过 {abs(int(diff_new_year))} 天"
    else:
        result["result"]["holiday"]["new_year_day"] = f"还有 {diff_new_year} 天"

    spring_festival_month_day = res.xpath('//*[@id="fjb_id"]/tr[3]/td[2]')[0].text
    spring_festival_month, spring_festival_day = re.findall(patt, spring_festival_month_day)[0]
    spring_festival_month = int(spring_festival_month) if spring_festival_month.isdigit() else 1
    spring_festival_day = int(spring_festival_day) if spring_festival_day.isdigit() else 1
    spring_festival = datetime.date(now_year, spring_festival_month, spring_festival_day)
    diff_spring_festival = str(spring_festival - now).split(" ")[0]
    if "-" in diff_spring_festival:
        result["result"]["holiday"]["spring_festival"] = f"已过 {abs(int(diff_spring_festival))} 天"
    else:
        result["result"]["holiday"]["spring_festival"] = f"还有 {diff_spring_festival} 天"

    tomb_sweeping_month_day = res.xpath('//*[@id="fjb_id"]/tr[4]/td[2]')[0].text
    tomb_sweeping_month, tomb_sweeping_day = re.findall(patt, tomb_sweeping_month_day)[0]
    tomb_sweeping_month = int(tomb_sweeping_month) if tomb_sweeping_month.isdigit() else 1
    tomb_sweeping_day = int(tomb_sweeping_day) if tomb_sweeping_day.isdigit() else 1
    tomb_sweeping = datetime.date(now_year, tomb_sweeping_month, tomb_sweeping_day)
    diff_tomb_sweeping = str(tomb_sweeping - now).split(" ")[0]
    if "-" in diff_tomb_sweeping:
        result["result"]["holiday"]["tomb_sweeping"] = f"已过 {abs(int(diff_tomb_sweeping))} 天"
    else:
        result["result"]["holiday"]["tomb_sweeping"] = f"还有 {diff_tomb_sweeping} 天"

    labour_day_month_day = res.xpath('//*[@id="fjb_id"]/tr[5]/td[2]')[0].text
    labour_day_month, labour_day_day = re.findall(patt, labour_day_month_day)[0]
    labour_day_month = int(labour_day_month) if labour_day_month.isdigit() else 1
    labour_day_day = int(labour_day_day) if labour_day_day.isdigit() else 1
    labour_day = datetime.date(now_year, labour_day_month, labour_day_day)
    diff_labour_day = str(labour_day - now).split(" ")[0]
    if "-" in diff_labour_day:
        result["result"]["holiday"]["labour_day"] = f"已过 {abs(int(diff_labour_day))} 天"
    else:
        result["result"]["holiday"]["labour_day"] = f"还有 {diff_labour_day} 天"

    dragon_boat_month_day = res.xpath('//*[@id="fjb_id"]/tr[6]/td[2]')[0].text
    dragon_boat_month, dragon_boat_day = re.findall(patt, dragon_boat_month_day)[0]
    dragon_boat_month = int(dragon_boat_month) if dragon_boat_month.isdigit() else 1
    dragon_boat_day = int(dragon_boat_day) if dragon_boat_day.isdigit() else 1
    dragon_boat = datetime.date(now_year, dragon_boat_month, dragon_boat_day)
    diff_dragon_boat = str(dragon_boat - now).split(" ")[0]
    if "-" in diff_dragon_boat:
        result["result"]["holiday"]["dragon_boat"] = f"已过 {abs(int(diff_dragon_boat))} 天"
    else:
        result["result"]["holiday"]["dragon_boat"] = f"还有 {diff_dragon_boat} 天"

    national_month_day = res.xpath('//*[@id="fjb_id"]/tr[7]/td[2]')[0].text
    national_month, national_day = re.findall(patt, national_month_day)[0]
    national_month = int(national_month) if national_month.isdigit() else 1
    national_day = int(national_day) if national_day.isdigit() else 1
    national = datetime.date(now_year, national_month, national_day)
    diff_national = str(national - now).split(" ")[0]
    if "-" in diff_national:
        result["result"]["holiday"]["national"] = f"已过 {abs(int(diff_national))} 天"
    else:
        result["result"]["holiday"]["national"] = f"还有 {diff_national} 天"

    autumn_month_day = res.xpath('//*[@id="fjb_id"]/tr[8]/td[2]')[0].text
    autumn_month, autumn_day = re.findall(patt, autumn_month_day)[0]
    autumn_month = int(autumn_month) if autumn_month.isdigit() else 1
    autumn_day = int(autumn_day) if autumn_day.isdigit() else 1
    autumn = datetime.date(now_year, autumn_month, autumn_day)
    diff_autumn = str(autumn - now).split(" ")[0]
    if "-" in diff_autumn:
        result["result"]["holiday"]["autumn"] = f"已过 {abs(int(diff_autumn))} 天"
    else:
        result["result"]["holiday"]["autumn"] = f"还有 {diff_autumn} 天"

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
