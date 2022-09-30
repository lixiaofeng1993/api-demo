import hmac
import urllib.parse
import hashlib
import base64
import requests
import urllib3
import time
from public.log import logger

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


def send_ding(body: dict):
    """
    发送钉钉消息
    :param body
    :return:
    """
    headers = {"Content-Type": "application/json"}
    access_token = "dfb892d96c26718f34f10fb494b463e28fb41049250a9a15f5fd8ebc50e7d1ca"
    timestamp, sign = ding_sign()

    res = requests.post(
        "https://oapi.dingtalk.com/robot/send?access_token={}&timestamp={}&sign={}".format(
            access_token, timestamp, sign), headers=headers, json=body, verify=False).json()
    if res["errcode"] == 0 and res["errmsg"] == "ok":
        logger.info("钉钉通知发送成功！info：{}".format(body["text"]["content"]))
    else:
        logger.error("钉钉通知发送失败！返回值：{}".format(res))
