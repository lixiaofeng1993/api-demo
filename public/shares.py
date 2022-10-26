#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: shares.py
# 创建时间: 2022/9/30 0030 18:35
# @Version：V 0.1
# @desc :
import time
import matplotlib.pyplot as plt
import efinance as ef
from datetime import datetime, date
from chinese_calendar import is_workday

from sql_app.database import SessionLocal
from public.send_ding import send_ding
from sql_app import crud_shares
from conf.settings import SHARES
from public.log import logger, BASE_PATH, os


def shares(stock_code: str = ""):
    make = False
    if not stock_code:
        stock_code = "601069"
    else:
        make = True
        stock_code = stock_code
    year = date.today().year
    month = date.today().month
    day = date.today().day
    now_time = datetime.now()
    now_img = int(round(time.time() * 1000))
    weekday = date(year, month, day).strftime("%A")
    if (not is_workday(date(year, month, day)) or weekday in ["Saturday", "Sunday"]) and not make:
        logger.info(f"当前时间 {now_time} 休市日!!!")
        return
    start_time = datetime(year, month, day, 9, 15, 0)
    end_time = datetime(year, month, day, 15, 5, 0)
    am_time = datetime(year, month, day, 11, 35, 0)
    pm_time = datetime(year, month, day, 13, 00, 0)
    save_time = datetime(year, month, day, 15, 0, 0)
    if (now_time < start_time or now_time > end_time or am_time < now_time < pm_time) and not make:
        logger.info(f"当前时间 {now_time} 未开盘!!!")
        return
    # 数据间隔时间为 1 分钟
    freq = 1
    # 获取最新一个交易日的分钟级别股票行情数据
    df = ef.stock.get_quote_history(stock_code, klt=freq)
    if df.empty:
        logger.info(f"当前时间 {now_time} 未获取到股票数据!!!")
        return
    if not make:
        # 绘制图形
        logger.info(f"当前时间戳: {now_img}")
        plt.plot(df["开盘"].values, linewidth=1, color="red")
        plt.savefig(os.path.join(BASE_PATH, "media", f"Chart-{now_img}.jpg"), bbox_inches='tight')
        plt.clf()

    max_price, min_price, avg_price, so_day = "", "", "", ""
    share_name = df["股票名称"].values[0]
    with SessionLocal() as db:
        asc_data = crud_shares.get_shares_by_name(db, share_name, flag=True)
        desc_data = crud_shares.get_shares_by_name(db, share_name)
    if asc_data:
        # so_day = (now_time - asc_data.date_time)
        day_list = crud_shares.get_shares_days(db, share_name)
        _day_list = list()
        for day in day_list:
            _day_list.append(day[0].strftime("%Y-%m-%d"))
        so_day = len(set(_day_list))
        max_price, min_price, avg_price = crud_shares.get_shares_avg(db, share_name)
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
    max_price_color = "#FF0000" if max_price > top_price else "#00FF00"
    avg_price_color = "#FF0000" if avg_price > average else "#00FF00"
    min_price_color = "#FF0000" if min_price > down_price else "#00FF00"

    if make:
        data = f"{share_name}\n开盘价：{open_price} 元/股\n最高价：{top_price} 元/股\n最低价：{down_price} 元/股\n" \
               f"平均价：{average} 元/股\n涨跌幅：{rise_and_fall} %\n涨跌额：{rise_and_price} 元\n成交量：{turnover} 手\n" \
               f"换手率：{turnover_rate} %\n时间：{new_time} \n最新价：{new_price} 元/股"
        if so_day:
            data += f"\n\n历史 {so_day} 天最高价：{max_price} 元/股\n历史 {so_day} 天平均价：{avg_price} 元/股\n" \
                    f"历史 {so_day} 天最低价：{min_price} 元/股"
        return data
    # f"> **状态** <font>开盘中</font> \n\n"
    body = {
        "msgtype": "markdown",
        "markdown": {
            "title": share_name,
            "text": f"### {share_name}\n\n"
                    f"> **开盘价** <font>{open_price}</font> 元/股\n\n"
                    f"> **最高价** <font color={top_price_color}>{top_price}</font> 元/股\n\n"
                    f"> **最低价** <font color={down_price_color}>{down_price}</font> 元/股\n\n"
                    f"> **平均价** <font color=''>{average}</font> 元/股\n\n"
                    f"> **涨跌幅** <font color={rise_and_fall_color}>{rise_and_fall}</font> %\n\n"
                    f"> **涨跌额** <font color={rise_and_price_color}>{rise_and_price}</font> 元\n\n"
                    f"> **成交量** <font>{turnover}</font> 手\n\n"
                    f"> **换手率** <font>{turnover_rate}</font> %\n\n"
                    f"> **时间** <font>{new_time}</font>\n\n"
                    f"> **最新价** <font color={new_price_color}>{new_price}</font> 元/股\n\n"
                    f"> **折线图:** ![screenshot](http://121.41.54.234/Chart-{now_img}.jpg)\n\n"
                    f"> **历史 {so_day} 天最高价** <font color={max_price_color}>{max_price}</font> 元/股\n\n"
                    f"> **历史 {so_day} 天平均价** <font color='{avg_price_color}'>{avg_price}</font> 元/股\n\n"
                    f"> **历史 {so_day} 天最低价** <font color={min_price_color}>{min_price}</font> 元/股 @15235514553\n\n"
        },
        "at": {
            "atMobiles": ["15235514553"],
            "isAtAll": False,
        }}

    if not desc_data:
        save = True
    elif desc_data and (now_time - desc_data.date_time).days and end_time > now_time > save_time:
        save = True
    else:
        save = False
    if save:
        df_list = df.to_dict(orient="records")
        shares_list = []
        for data in df_list:
            shares_dict = dict()
            for key, value in SHARES.items():
                shares_dict.update({
                    key: data[value]
                })
            shares_list.append(shares_dict)
        crud_shares.add_all_shares(db, shares_list)
        logger.info(f"股票： {share_name} 日期：{now_time} ==> 批量保存成功！")
    send_ding(body)
