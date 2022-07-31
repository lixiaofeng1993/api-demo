#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/29 19:23
# @Author  : lixiaofeng
# @Site    : 
# @File    : calendar.py
# @Software: PyCharm

import re
import datetime
import requests
from fastapi import Depends, APIRouter
from requests_html import HTMLSession

router = APIRouter()


@router.get("/", summary="解析html数据")
def get_calendar():
    result = {
        "公告": "【摸鱼办宣】",
        "今天": {},
        "放假安排": {},
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
    result["今天"]["公历日期"] = res.xpath('//div[@id="textbody"]/p/table/tr[1]/td[2]', first=True).text
    result["今天"]["农历日期"] = res.xpath('//div[@id="textbody"]/p/table/tr[2]/td[2]', first=True).text
    week_day = res.xpath('//div[@id="textbody"]/p/table/tr[3]/td[2]', first=True).text
    result["今天"]["星　　期"] = week_day
    result["今天"]["星　　座"] = res.xpath('//div[@id="textbody"]/p/table/tr[4]/td[2]', first=True).text
    result["今天"]["季　　节"] = res.xpath('//div[@id="textbody"]/p/table/tr[5]/td[2]', first=True).text
    result["今天"]["节　　气"] = res.xpath('//div[@id="textbody"]/p/table/tr[6]/td[2]', first=True).text
    result["今天"]["节　　日"] = res.xpath('//div[@id="textbody"]/p/table/tr[7]/td[2]', first=True).text
    result["今天"]["三伏数九"] = res.xpath('//div[@id="textbody"]/p/table/tr[8]/td[2]', first=True).text
    result["今天"]["今日所宜"] = res.xpath('//div[@id="textbody"]/p/table/tr[11]/td[2]', first=True).text
    result["今天"]["今日所忌"] = res.xpath('//div[@id="textbody"]/p/table/tr[12]/td[2]', first=True).text
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
        result["放假安排"]["周末"] = f"还有 {week[week_day]} 天"
    else:
        result["放假安排"]["周末"] = "当前是周末，要好好享受生活丫~"
    if "-" in diff_new_year:

        result["放假安排"]["元旦"] = f"已过 {abs(int(diff_new_year))} 天"
    else:
        result["放假安排"]["元旦"] = f"还有 {diff_new_year} 天"

    spring_festival_month_day = res.xpath('//*[@id="fjb_id"]/tr[3]/td[2]')[0].text
    spring_festival_month, spring_festival_day = re.findall(patt, spring_festival_month_day)[0]
    spring_festival_month = int(spring_festival_month) if spring_festival_month.isdigit() else 1
    spring_festival_day = int(spring_festival_day) if spring_festival_day.isdigit() else 1
    spring_festival = datetime.date(now_year, spring_festival_month, spring_festival_day)
    diff_spring_festival = str(spring_festival - now).split(" ")[0]
    if "-" in diff_spring_festival:
        result["放假安排"]["春节"] = f"已过 {abs(int(diff_spring_festival))} 天"
    else:
        result["放假安排"]["春节"] = f"还有 {diff_spring_festival} 天"

    tomb_sweeping_month_day = res.xpath('//*[@id="fjb_id"]/tr[4]/td[2]')[0].text
    tomb_sweeping_month, tomb_sweeping_day = re.findall(patt, tomb_sweeping_month_day)[0]
    tomb_sweeping_month = int(tomb_sweeping_month) if tomb_sweeping_month.isdigit() else 1
    tomb_sweeping_day = int(tomb_sweeping_day) if tomb_sweeping_day.isdigit() else 1
    tomb_sweeping = datetime.date(now_year, tomb_sweeping_month, tomb_sweeping_day)
    diff_tomb_sweeping = str(tomb_sweeping - now).split(" ")[0]
    if "-" in diff_tomb_sweeping:
        result["放假安排"]["清明节"] = f"已过 {abs(int(diff_tomb_sweeping))} 天"
    else:
        result["放假安排"]["清明节"] = f"还有 {diff_tomb_sweeping} 天"

    labour_day_month_day = res.xpath('//*[@id="fjb_id"]/tr[5]/td[2]')[0].text
    labour_day_month, labour_day_day = re.findall(patt, labour_day_month_day)[0]
    labour_day_month = int(labour_day_month) if labour_day_month.isdigit() else 1
    labour_day_day = int(labour_day_day) if labour_day_day.isdigit() else 1
    labour_day = datetime.date(now_year, labour_day_month, labour_day_day)
    diff_labour_day = str(labour_day - now).split(" ")[0]
    if "-" in diff_labour_day:
        result["放假安排"]["劳动节"] = f"已过 {abs(int(diff_labour_day))} 天"
    else:
        result["放假安排"]["劳动节"] = f"还有 {diff_labour_day} 天"

    dragon_boat_month_day = res.xpath('//*[@id="fjb_id"]/tr[6]/td[2]')[0].text
    dragon_boat_month, dragon_boat_day = re.findall(patt, dragon_boat_month_day)[0]
    dragon_boat_month = int(dragon_boat_month) if dragon_boat_month.isdigit() else 1
    dragon_boat_day = int(dragon_boat_day) if dragon_boat_day.isdigit() else 1
    dragon_boat = datetime.date(now_year, dragon_boat_month, dragon_boat_day)
    diff_dragon_boat = str(dragon_boat - now).split(" ")[0]
    if "-" in diff_dragon_boat:
        result["放假安排"]["端午节"] = f"已过 {abs(int(diff_dragon_boat))} 天"
    else:
        result["放假安排"]["端午节"] = f"还有 {diff_dragon_boat} 天"

    national_month_day = res.xpath('//*[@id="fjb_id"]/tr[7]/td[2]')[0].text
    national_month, national_day = re.findall(patt, national_month_day)[0]
    national_month = int(national_month) if national_month.isdigit() else 1
    national_day = int(national_day) if national_day.isdigit() else 1
    national = datetime.date(now_year, national_month, national_day)
    diff_national = str(national - now).split(" ")[0]
    if "-" in diff_national:
        result["放假安排"]["中秋节"] = f"已过 {abs(int(diff_national))} 天"
    else:
        result["放假安排"]["中秋节"] = f"还有 {diff_national} 天"

    autumn_month_day = res.xpath('//*[@id="fjb_id"]/tr[8]/td[2]')[0].text
    autumn_month, autumn_day = re.findall(patt, autumn_month_day)[0]
    autumn_month = int(autumn_month) if autumn_month.isdigit() else 1
    autumn_day = int(autumn_day) if autumn_day.isdigit() else 1
    autumn = datetime.date(now_year, autumn_month, autumn_day)
    diff_autumn = str(autumn - now).split(" ")[0]
    if "-" in diff_autumn:
        result["放假安排"]["国庆节"] = f"已过 {abs(int(diff_autumn))} 天"
    else:
        result["放假安排"]["国庆节"] = f"还有 {diff_autumn} 天"

    return result


@router.get("/v1", summary="万年历api接口")
def get_calendar():
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
