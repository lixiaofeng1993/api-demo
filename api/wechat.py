#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
# 创 建 人: 李先生
# 文 件 名: wechat.py.py
# 创建时间: 2022/10/14 0014 21:52
# 版   本：V 0.1
# 说   明: 
"""

import hashlib
import requests
import aiohttp

from fastapi import Depends, APIRouter, HTTPException, status, Request, Body
from starlette.responses import HTMLResponse, Response

from sql_app.database import Base, engine
from public.custom_code import result
from conf.settings import TOKEN, AppID, AppSecret, FOLLOW
from public.wx_message import parse_xml, Message
from public.shares import shares
from public.wx_img import wx_media
from public.log import logger

Base.metadata.create_all(bind=engine)  # 生成数据库

router = APIRouter()


@router.get("/", summary="微信服务器配置验证")
async def handle_wx(signature, timestamp, nonce, echostr):
    try:
        temp = [TOKEN, timestamp, nonce]
        temp.sort()
        hashcode = hashlib.sha1("".join(temp).encode('utf-8')).hexdigest()
        logger.info(f"加密：{hashcode}，微信返回：{signature}")
        if hashcode == signature:
            return int(echostr)
        else:
            logger.error("加密字符串 不等于 微信返回字符串，验证失败！！！")
            return "验证失败！"
    except Exception as error:
        return f"微信服务器配置验证出现异常:{error}"


@router.post("/", summary="回复微信消息")
async def wx_msg(request: Request, signature, timestamp, nonce, openid):
    temp = [TOKEN, timestamp, nonce]
    temp.sort()
    hashcode = hashlib.sha1("".join(temp).encode('utf-8')).hexdigest()
    logger.info(f"加密：{hashcode}，微信返回：{signature}")
    if hashcode == signature:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("http://121.41.54.234/wx/login") as resp:
                    res = await resp.json()
            token = res["result"]["access_token"]
        except Exception as error:
            logger.error(f"获取微信登录token出现异常：{error}")
            token = ""
        try:
            rec_msg = parse_xml(await request.body())
            to_user = rec_msg.FromUserName
            from_user = rec_msg.ToUserName
            if rec_msg.MsgType == 'text':
                logger.info(f"文本信息：{rec_msg.Content}")
                if rec_msg.Content in ["图片", "小七"] and token:
                    media_id = wx_media(token)
                    return Response(
                        Message(to_user, from_user, media_id=media_id, msg_type="image").send(),
                        media_type="application/xml")
                content = shares(stock_code=rec_msg.Content)
                if content:
                    return Response(
                        Message(to_user, from_user, content=content).send(),
                        media_type="application/xml")
                else:
                    return Response(
                        Message(to_user, from_user, content=rec_msg.Content).send(),
                        media_type="application/xml")
            elif rec_msg.MsgType == 'event':
                return Response(
                    Message(to_user, from_user, content=FOLLOW).send(), media_type="application/xml")
            elif rec_msg.MsgType == "image":
                if token:
                    media_id = wx_media(token)
                else:
                    media_id = rec_msg.MediaId
                return Response(
                    Message(to_user, from_user, media_id=media_id, msg_type="image").send(),
                    media_type="application/xml")
        except Exception as error:
            logger.error(f"微信回复信息报错：{error}")
            return HTMLResponse('success')


@router.get("/login", summary="微信登录接口", description="微信登录接口")
async def login(request: Request):
    wx_token = await request.app.state.redis.get("wx_token")
    if wx_token:
        result["result"] = {"access_token": wx_token}
        return result
    else:
        url = f" https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={AppID}&secret={AppSecret}"
        try:
            res = requests.get(url=url).json()
            if "access_token" in res.keys():
                await request.app.state.redis.setex(key="wx_token", value=res["access_token"],
                                                    seconds=res["expires_in"])
                result["result"] = {"access_token": res["access_token"]}
            else:
                result["result"] = {"access_token": res}
            return result
        except Exception as error:
            result["result"] = error
            return result


@router.post("/rid", summary="获取rid信息", description="获取rid信息")
async def menu_create(rid: str):
    async with aiohttp.ClientSession() as session:
        async with session.get("http://127.0.0.1:8000/wx/login") as resp:
            res = await resp.json()
    token = res["result"]["access_token"]
    body = {
        "rid": rid
    }
    res = requests.post(f"https://api.weixin.qq.com/cgi-bin/openapi/rid/get?access_token={token}", json=body)
    return res.json()
