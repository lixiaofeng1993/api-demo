#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: get_daily_billboard.py
# 创建时间: 2022/11/5 0005 11:15
# @Version：V 0.1
# @desc :
import pandas as pd
import requests
from datetime import datetime, timedelta
from tqdm import tqdm
from typing import Dict, List, Union
from jsonpath import jsonpath

session = requests.Session()
EASTMONEY_STOCK_DAILY_BILL_BOARD_FIELDS = {
    'SECURITY_CODE': '股票代码',
    'SECURITY_NAME_ABBR': '股票名称',
    'TRADE_DATE': '上榜日期',
    'EXPLAIN': '解读',
    'CLOSE_PRICE': '收盘价',
    'CHANGE_RATE': '涨跌幅',
    'TURNOVERRATE': '换手率',
    'BILLBOARD_NET_AMT': '龙虎榜净买额',
    'BILLBOARD_BUY_AMT': '龙虎榜买入额',
    'BILLBOARD_SELL_AMT': '龙虎榜卖出额',
    'BILLBOARD_DEAL_AMT': '龙虎榜成交额',
    'ACCUM_AMOUNT': '市场总成交额',
    'DEAL_NET_RATIO': '净买额占总成交比',
    'DEAL_AMOUNT_RATIO': '成交额占总成交比',
    'FREE_MARKET_CAP': '流通市值',
    'EXPLANATION': '上榜原因'
}


def get_daily_billboard(start_date: str = None,
                        end_date: str = None) -> pd.DataFrame:
    """
    获取指定日期区间的龙虎榜详情数据

    Parameters
    ----------
    start_date : str, optional
        开始日期
        部分可选示例如下

        - ``None`` 最新一个榜单公开日(默认值)
        - ``"2021-08-27"`` 2021年8月27日

    end_date : str, optional
        结束日期
        部分可选示例如下

        - ``None`` 最新一个榜单公开日(默认值)
        - ``"2021-08-31"`` 2021年8月31日

    Returns
    -------
    DataFrame
        龙虎榜详情数据

    """
    today = datetime.today().date()
    mode = 'auto'
    if start_date is None:
        start_date = today

    if end_date is None:
        end_date = today

    if isinstance(start_date, str):
        mode = 'user'
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if isinstance(end_date, str):
        mode = 'user'
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    fields = EASTMONEY_STOCK_DAILY_BILL_BOARD_FIELDS
    bar: tqdm = None

    while 1:

        dfs: List[pd.DataFrame] = []
        page = 1
        while 1:
            params = (
                ('sortColumns', 'TRADE_DATE,SECURITY_CODE'),
                ('sortTypes', '-1,1'),
                ('pageSize', '500'),
                ('pageNumber', page),
                ('reportName', 'RPT_DAILYBILLBOARD_DETAILS'),
                ('columns', 'ALL'),
                ('source', 'WEB'),
                ('client', 'WEB'),
                ('filter',
                 f"(TRADE_DATE<='{end_date}')(TRADE_DATE>='{start_date}')"),
            )

            url = 'http://datacenter-web.eastmoney.com/api/data/v1/get'

            response = session.get(url, params=params)
            if bar is None:
                pages = jsonpath(response.json(), '$..pages')

                if pages and pages[0] != 1:
                    total = pages[0]
                    bar = tqdm(total=int(total))
            if bar is not None:
                bar.update()

            items = jsonpath(response.json(), '$..data[:]')
            if not items:
                break
            page += 1
            df = pd.DataFrame(items).rename(columns=fields)[fields.values()]
            dfs.append(df)
        if mode == 'user':
            break
        if len(dfs) == 0:
            start_date = start_date - timedelta(1)
            end_date = end_date - timedelta(1)

        if len(dfs) > 0:
            break
    if len(dfs) == 0:
        df = pd.DataFrame(columns=set(fields.values()))
        return df

    df = pd.concat(dfs, ignore_index=True)
    df['上榜日期'] = df['上榜日期'].astype('str').apply(lambda x: x.split(' ')[0])
    return df


if __name__ == '__main__':
    start = "2022-11-04"
    end = "2022-11-04"
    print(get_daily_billboard(start_date=start, end_date=end))
