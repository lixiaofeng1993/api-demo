#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
# 创 建 人: 李先生
# 文 件 名: shares.py
# 创建时间: 2022/9/30 0030 18:35
# 版   本：V 0.1
# 说   明: 
"""
from datetime import datetime, date
import efinance as ef
from chinese_calendar import is_workday
import matplotlib.pyplot as plt
import time

from public.send_ding import send_ding
from public.log import logger, BASE_PATH, os


def shares():
    year = date.today().year
    month = date.today().month
    day = date.today().day
    now_time = datetime.now()
    weekday = date(year, month, day).strftime("%A")
    if not is_workday(date(year, month, day)) or weekday in ["Saturday", "Sunday"]:
        logger.info(f"当前时间 {now_time} 休市日!!!")
        return
    start_time = datetime(year, month, day, 9, 15, 0)
    end_time = datetime(year, month, day, 15, 5, 0)
    am_time = datetime(year, month, day, 11, 35, 0)
    pm_time = datetime(year, month, day, 13, 00, 0)
    if now_time < start_time or now_time > end_time or am_time < now_time < pm_time:
        logger.info(f"当前时间 {now_time} 未开盘!!!")
        return
    stock_code = "601069"
    # 数据间隔时间为 1 分钟
    freq = 1
    # 获取最新一个交易日的分钟级别股票行情数据
    df = ef.stock.get_quote_history(stock_code, klt=freq)
    if df.empty:
        logger.info(f"当前时间 {now_time} 未获取到股票数据!!!")
        return
    # 绘制图形
    now_img = int(round(time.time() * 1000))
    logger.info(f"当前时间戳: {now_img}")
    plt.plot(df["开盘"].values, linewidth=1, color="red")
    plt.savefig(os.path.join(BASE_PATH, "media", f"Chart-{now_img}.jpg"), bbox_inches='tight')
    plt.clf()

    share_name = df["股票名称"].values[0]
    open_price = df["开盘"].values[0]
    new_price = df["收盘"].values[-1]
    new_time = df["日期"].values[-1]
    top_price = df["最高"].max()
    down_price = df["最低"].min()
    turnover = df["成交量"].sum()
    average = round(df["开盘"].mean(), 2)
    rise_and_fall = round(df["涨跌幅"].sum(), 2)
    rise_and_price = round(df["涨跌额"].sum(), 2)
    turnover_rate = round(df["换手率"].sum(), 2)
    rise_and_fall_color = "#FF0000" if rise_and_fall > 0 else "#00FF00"
    rise_and_price_color = "#FF0000" if rise_and_price > 0 else "#00FF00"
    new_price_color = "#FF0000" if new_price > open_price else "#00FF00"
    top_price_color = "#FF0000" if top_price > open_price else "#00FF00"
    down_price_color = "#FF0000" if down_price > open_price else "#00FF00"

    body = {
        "msgtype": "markdown",
        "markdown": {
            "title": share_name,
            "text": f"### {share_name}\n\n"
                    f"> **开盘价:** <font>{open_price}</font> 元/股\n\n"
                    f"> **最高价:** <font color={top_price_color}>{top_price}</font> 元/股\n\n"
                    f"> **最低价:** <font color={down_price_color}>{down_price}</font> 元/股\n\n"
                    f"> **平均价:** <font color=''>{average}</font> 元/股\n\n"
                    f"> **涨跌幅:** <font color={rise_and_fall_color}>{rise_and_fall}</font> %\n\n"
                    f"> **涨跌额:** <font color={rise_and_price_color}>{rise_and_price}</font> 元\n\n"
                    f"> **成交量:** <font>{turnover}</font> 手\n\n"
                    f"> **换手率:** <font>{turnover_rate}</font> %\n\n"
                    f"> **时间:** <font>{new_time}</font>\n\n"
                    f"> **最新价:** <font color={new_price_color}>{new_price}</font> 元/股\n\n"
                    f"> **状态:** <font>开盘中</font> \n\n"
                    f"> **折线图:** ![screenshot](http://121.41.54.234/Chart-{now_img}.jpg) @15235514553\n\n"
        },
        "at": {
            "atMobiles": ["15235514553"],
            "isAtAll": False,
        }}
    send_ding(body)
