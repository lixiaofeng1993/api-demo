import hmac
import urllib.parse
import hashlib
import base64
import requests
import urllib3
import time
from datetime import datetime, date
import efinance as ef
from loguru import logger

urllib3.disable_warnings()


def ding_sign():
    """
    发送钉钉消息加密
    :return:
    """
    timestamp = str(round(time.time() * 1000))
    secret = "SEC4abe8f6887a15a96ff1e8358e8ee0602025a0cb2f73a4c46c1105cbe9424250c"
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return timestamp, sign


def send_ding():
    """
    发送钉钉消息
    :param content:
    :return:
    """
    headers = {"Content-Type": "application/json"}
    access_token = "dfb892d96c26718f34f10fb494b463e28fb41049250a9a15f5fd8ebc50e7d1ca"
    timestamp, sign = ding_sign()

    year = date.today().year
    month = date.today().month
    day = date.today().day
    start_time = datetime(year, month, day, 9, 30, 0)
    end_time = datetime(year, month, day, 15, 00, 0)
    now_time = datetime.now()
    status = ""
    if start_time <= now_time <= end_time:
        status = "开盘中"
    elif now_time < start_time:
        status = "未开盘"
    elif now_time > end_time:
        status = "已收盘"
    stock_code = "601069"
    # 数据间隔时间为 1 分钟
    freq = 1
    # 获取最新一个交易日的分钟级别股票行情数据
    df = ef.stock.get_quote_history(stock_code, klt=freq)
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

    body = {
        "msgtype": "text",
        "text": {
            "content": f"股票名称：{share_name} \n【开盘价】 {open_price} 元/股\n【最高价】 {top_price} 元/股\n【最低价】 {down_price} 元/股 \n"
                       f"【平均价】 {average} 元/股\n【涨跌幅】 {rise_and_fall} %\n【涨跌额】 {rise_and_price} 元\n"
                       f"【成交量】 {turnover} 手\n【换手率】 {turnover_rate} % \n【最新价】 {new_price} 元/股\n"
                       f"【时间】 {new_time}\n【状态】 {status}"
        }
    }
    res = requests.post(
        "https://oapi.dingtalk.com/robot/send?access_token={}&timestamp={}&sign={}".format(
            access_token, timestamp, sign), headers=headers, json=body, verify=False).json()
    if res["errcode"] == 0 and res["errmsg"] == "ok":
        logger.info("钉钉通知发送成功！info：{}".format(body["text"]["content"]))
    else:
        logger.error("钉钉通知发送失败！返回值：{}".format(res))
