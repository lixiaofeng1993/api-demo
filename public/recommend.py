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

from conf.settings import GAO_KEY, CITY_CODE, IDIOM_KEY, IDIOM_INFO
from public.log import logger


def get_weather():
    params = {
        "key": f"{GAO_KEY}",
        "city": f"{CITY_CODE}",
        "extensions": "base",
        "output": "JSON",
    }
    res = requests.get("https://restapi.amap.com/v3/weather/weatherInfo", params=params, verify=False)
    res.encoding = "utf-8"
    weather = jsonpath(res.json(), "$.lives[*].weather")
    return weather[0] if weather else ""


def now_season():
    season = ""
    month = date.today().month
    if month in [3, 4, 5]:
        season = ["春天", "清明节", "寒食节"]
    elif month in [6, 7, 8]:
        season = ["夏天", "七夕节", "端午节"]
    elif month in [9, 10, 11]:
        season = ["秋天", "中秋节", "重阳节"]
    elif month in [12, 1, 2]:
        season = ["冬天", "元宵节", "春节"]
    return season


def recommend_handle():
    weather = get_weather()
    if "晴" in weather:
        type_list = ["西湖", "爱情", "友情", "抒情"]
    elif "雨" in weather:
        type_list = ["写雨", "思乡", "离别", "伤感", "送别"]
    elif "风" in weather:
        type_list = ["写风", "柳树", "桃花", "菊花", "忧民"]
    elif "雪" in weather:
        type_list = ["写雪", "梅花"]
    elif "阴" in weather:
        type_list = ["小窗幽记", "闺怨", "怀古"]
    elif "云" in weather:
        type_list = ["星星", "月亮", "写云"]
    elif "雾" in weather:
        type_list = ["田园", "泰山", "庐山"]
    elif "沙" in weather:
        type_list = ["感恩", "哲理", "边塞"]
    else:
        type_list = ["史记", "国语", "吕氏春秋", "贞观政要", "围炉夜话"]
    type_list.extend(now_season())
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
    if not data_list:
        content += f"emmm，结束了嘿，么有找到 {last_word} 开头的成语。"
        return content
    content += f'最后一个字：{last_word}\n'
    for data in res["result"]["data"]:
        content += f"<a href='weixin://bizmsgmenu?msgmenucontent={data}&msgmenuid=9523'>{data}</a>\n"
    content += f">>> 点击成语 或者查看 <a href='weixin://bizmsgmenu?msgmenucontent=IDIOM-INFO-{text}&msgmenuid={text}'>{text}</a>"
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
    print(idiom_info("寅吃卯粮"))
