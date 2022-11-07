#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: stock_recommend.py
# 创建时间: 2022/11/6 0006 17:45
# @Version：V 0.1
# @desc :
import efinance as ef
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pandas import DataFrame

from public.get_daily_billboard import get_daily_billboard

now_time = datetime.now()


def get_daily_billboard_list():
    """
    股票龙虎榜
    :return:
    """
    daily_billboard = get_daily_billboard()
    daily_billboard_list = []
    for daily in zip(daily_billboard["股票名称"], daily_billboard["上榜原因"]):
        daily_billboard_list.append(daily)
    return daily_billboard_list


def shares_avg(code: str = "西部黄金", klt: int = 101, beg: str = ""):
    """
    股票均价
    :param code: 股票名称
    :param klt: 粒度 101 天 60 分钟
    :param beg: 开始时间
    :return:
    """
    now_time_str = now_time.strftime("%Y%m%d")
    quote_history = ef.stock.get_quote_history(code, klt=klt, beg=beg, end=now_time_str)
    # quote_history.to_csv("1.csv")
    # top_price = quote_history["最高"].max()
    # down_price = quote_history["最低"].min()
    # average_close = round(quote_history["收盘"].mean(), 2)
    turnover = quote_history["成交量"].sum()
    turnover_price = round(quote_history["成交额"].sum(), 2)
    average = round(turnover_price / (turnover * 100), 2)
    return average


def stock_analysis(data: DataFrame):
    # time_60 = (now_time + relativedelta(days=-76)).strftime("%Y%m%d")
    # time_10 = (now_time + relativedelta(days=-12)).strftime("%Y%m%d")
    # time_5 = (now_time + relativedelta(days=-7)).strftime("%Y%m%d")

    choice_list = []
    for index, row in data.iterrows():
        print(type(row))
        if "ST" in row["股票名称"]:
            continue
        if row["最新价"] > 18:
            continue
        if 2.5 >= row["量比"] >= 1.5:
            row = row.append(pd.Series({
                "状态": "量比"
            }))
            choice_list.append(row)
        # average_60 = shares_avg(r[0], beg=time_60)
        # average_10 = shares_avg(r[0], beg=time_10)
        # average_5 = shares_avg(r[0], beg=time_5)
        # average = shares_avg(r[0], klt=60)
        # choice_list.append(row)
    return choice_list


def stock():
    """
    量比=（现成交总手数/现累计开市时间(分)）/过去5日平均每分钟成交量
    量比反映出的主力行为从计算公式中可以看出，量比的数值越大，表明了该股当日流入的资金越多，市场活跃度越高；反之，量比值越小，说明了资金的流入越少，市场活跃度越低。
    一般来说，量比为0.8-1.5倍，则说明成交量处于正常水平；量比在1.5-2.5倍之间则为温和放量，我们选股多考虑量比在这一范围的个股
    :return:
    """
    daily_billboard_list = get_daily_billboard_list()
    df = ef.stock.get_realtime_quotes()
    df.drop(df.index[df["涨跌幅"] == "-"], inplace=True)
    df.drop(df.index[df["量比"] == "-"], inplace=True)
    df_down = df.sort_values(["涨跌幅", "成交量"], ascending=[True, False])
    df_down_100 = df_down[:20]

    df_top = df.sort_values(["涨跌幅", "成交量"], ascending=[False, False])
    df_top_100 = df_top[:20]
    df_top_100.to_csv("1.csv")
    choice_down_list = stock_analysis(df_down_100)[:5]
    choice_top_list = stock_analysis(df_top_100)[:5]
    content = "今日股票推荐：\n涨幅榜\n"
    for data in choice_top_list:
        print(data["状态"])
    #     content += f"<a href='weixin://bizmsgmenu?msgmenucontent={data['股票名称']}&msgmenuid=9530'>{data['股票名称']}</a> 最新价 {data['最新价']} 元/股\n"
    #     for daily_billboard in daily_billboard_list:
    #         if data['股票名称'] == daily_billboard[0]:
    #             content += f"龙虎榜：{daily_billboard[1]}\n"
    # content += "\n跌幅榜\n"
    # for data in choice_down_list:
    #     content += f"<a href='weixin://bizmsgmenu?msgmenucontent={data['股票名称']}&msgmenuid=9530'>{data['股票名称']}</a> 最新价 {data['最新价']} 元/股\n"
    #     for daily_billboard in daily_billboard_list:
    #         if data['股票名称'] == daily_billboard[0]:
    #             content += f"龙虎榜：{daily_billboard[1]}\n"
    return content


if __name__ == '__main__':
    print(stock())
