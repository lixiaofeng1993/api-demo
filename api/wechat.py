#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: wechat.py
# 创建时间: 2022/10/14 0014 21:52
# @Version：V 0.1
# @desc :
import requests
import aiohttp

from fastapi import Depends, APIRouter, HTTPException, status, Request, Body
from starlette.responses import HTMLResponse, Response
from sqlalchemy.orm import Session

from sql_app.database import Base, engine
from public.common import get_db
from public.custom_code import result
from conf.settings import AppID, AppSecret
from public.wx_message import parse_xml, Message
from public.wx_public import sign_sha1, send_wx_msg
from public.log import logger

Base.metadata.create_all(bind=engine)  # 生成数据库

router = APIRouter()


@router.get("/", summary="微信服务器配置验证")
async def handle_wx(signature, timestamp, nonce, echostr):
    try:
        if sign_sha1(signature, timestamp, nonce):
            return int(echostr)
        else:
            logger.error("加密字符串 不等于 微信返回字符串，验证失败！！！")
            return "验证失败！"
    except Exception as error:
        return f"微信服务器配置验证出现异常:{error}"


@router.post("/", summary="回复微信消息")
async def wx_msg(request: Request, signature, timestamp, nonce, openid, db: Session = Depends(get_db)):
    if sign_sha1(signature, timestamp, nonce):
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
            text = rec_msg.Content
            content, media_id, skip = "", "", ""
            if text:
                if text == "推荐":
                    content = await request.app.state.redis.get("recommended-today")
                elif text and ("DYNASTY" in text or "POETRY_TYPE" in text or "AUTHOR" in text or "RECOMMEND" in text):
                    skip = await request.app.state.redis.get(text)
                    if not skip:
                        content = "会话只有30分钟，想了解更多，请重新发起~"
                elif text in ["成语接龙", "接龙"]:
                    await request.app.state.redis.setex(key=f"IDIOM", value=text, seconds=30 * 60)
                    content = "进入时效30分钟的成语接龙时刻，输入成语开始吧~"
                elif text == "exit":
                    await request.app.state.redis.delete("IDIOM")
                    content = "See you later..."
            if not content:
                idiom = await request.app.state.redis.get("IDIOM")
                content, media_id = send_wx_msg(db, request, rec_msg, token, skip, idiom)
            if rec_msg.MsgType == 'text' and not media_id:
                if "</a>" in content and len(content) >= 2000:
                    content = "..." + content[len(content) - 2000:]
                elif len(content) >= 666 and "</a>" not in content:
                    content = content[:666] + "..."
                return Response(
                    Message(to_user, from_user, content=content).send(),
                    media_type="application/xml")
            elif rec_msg.MsgType == 'event' and content:
                return Response(
                    Message(to_user, from_user, content=content).send(), media_type="application/xml")
            elif rec_msg.MsgType == "image" or media_id:
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


@router.get("/test", summary="测试微信接口信息")
async def wx_test(text: str, request: Request, db: Session = Depends(get_db)):
    from public.wx_public import poetry_content

    data = poetry_content(db, request, text)
    print(data)
    return result
