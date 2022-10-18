#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
# 创 建 人: 李先生
# 文 件 名: poetry.py
# 创建时间: 2022/10/17 0017 19:41
# 版   本：V 0.1
# 说   明: 
"""
import re

from typing import List, Dict

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from requests_html import HTMLSession

from sql_app.schemas_users import User
from sql_app import crud_poetry
from public.custom_code import result
from dependencies import get_current_user_info
from public.public import get_db, json_format
from public.log import logger

router = APIRouter()


@router.get("/", summary="爬取古诗词")
def get_poetry(db: Session = Depends(get_db), user: User = Depends(get_current_user_info)):
    type_list = ['春天', '夏天', '秋天', '冬天', '爱国', '写雪', '思念', '爱情', '思乡', '离别', '月亮', '梅花', '励志', '荷花', '写雨', '友情', '感恩',
                 '写风', '西湖', '读书', '菊花', '长江', '黄河', '竹子', '哲理', '泰山', '边塞', '柳树', '写鸟', '桃花', '老师', '母亲', '伤感', '田园',
                 '写云', '庐山', '山水', '星星', '荀子', '孟子', '论语', '墨子', '老子', '史记', '中庸', '礼记', '尚书', '晋书', '左传', '论衡', '管子',
                 '说苑', '列子', '国语', '节日', '春节', '元宵节', '寒食节', '清明节', '端午节', '七夕节', '中秋节', '重阳节', '韩非子', '罗织经', '菜根谭',
                 '红楼梦', '弟子规', '战国策', '后汉书', '淮南子', '商君书', '水浒传', '西游记', '格言联璧', '围炉夜话', '增广贤文', '吕氏春秋', '文心雕龙', '醒世恒言',
                 '警世通言', '幼学琼林', '小窗幽记', '三国演义', '贞观政要']
    # type_list = ["贞观政要"]
    for tstr in type_list:
        for i in range(1, 5):
            with HTMLSession() as session:
                base_url = f"https://so.gushiwen.cn/mingjus/default.aspx?page={i}&tstr={tstr}&astr=&cstr=&xstr="
                res = session.get(base_url).html
            try:
                links = res.xpath('//*[@id="html"]/body/div[2]/div[1]/div[2]/div[1]/a[1]', first=True).links
            except Exception as error:
                logger.error(f"第一层 url 错误：{base_url} ==> {error}")
                continue
            details_links = []
            for link in links:
                if "/mingju/juv_" in link:
                    link = "https://so.gushiwen.cn" + link
                    details_links.append(link)
            for details_link in details_links:
                with HTMLSession() as session:
                    res = session.get(details_link).html
                    # res = session.get("https://so.gushiwen.cn/mingju/juv_8d8c88731d06.aspx").html
                phrase_text = res.xpath('/html/body/div[2]/div[1]/div[2]/div[1]', clean=True, first=True).text
                phrase_list = phrase_text.split("完善")[0].split("\n")
                phrase, explain, appreciation, backdrop, poetry_name = phrase_list[0], "", "", "", ""
                for text in phrase_list:
                    if "解释" in text:
                        explain = text.split("：")[-1]
                    if "赏析" in text:
                        appreciation = text.split("：")[-1]
                    if "摘自" in text:
                        poetry_name_patt = "《(.+)》"
                        poetry_name = re.findall(poetry_name_patt, text)[0]
                try:
                    original_text = res.xpath('/html/body/div[2]/div[1]/div[3]/div[1]', clean=True, first=True).text
                    name_patt = "原文\\s(.+)《"
                    poetry_name_patt = "《(.+)》"
                    original_patt = "》([\\s\\S]+?)译文"
                    name = re.findall(name_patt, original_text)[0]
                    poetry_name = re.findall(poetry_name_patt, original_text)[0]
                    original = re.findall(original_patt, original_text)[0].strip("\n")
                    translation_text = res.xpath('/html/body/div[2]/div[1]/div[4]/div[1]/p[1]', clean=True,
                                                 first=True).text
                    translation_patt = "译文([\\s\\S]+?)注释"
                    translation = re.findall(translation_patt, translation_text)[0].strip("\n")
                    # print(translation_text)
                    author_list = translation_text.split("猜您喜欢")[0].split("完善")
                    authors = []
                    for x in author_list:
                        if x and x != "\n":
                            authors.append(x)
                    author_data = authors[-1].split("\n")
                    _author = []
                    for x in author_data:
                        if x and x != "\n":
                            _author.append(x)
                    introduce = _author[-1].split("►")[0]
                    if name not in introduce:
                        introduce = ""
                except Exception as error:
                    logger.error(f"第二层url 错误：{error} ==> {details_link}")
                    poetry = crud_poetry.get_poetry_by_name(db, poetry_name)
                    if not poetry:
                        poetry = crud_poetry.create_poetry1(db, poetry={
                            "type": tstr,
                            "phrase": phrase,
                            "explain": explain,
                            "name": poetry_name,
                            "url": details_link,
                        })
                        logger.info(f"古诗：{poetry_name} 爬取成功！作者：无")
                        result["result"] += poetry_name + "\n"
                    continue
                author = crud_poetry.get_author_by_name(db, name)
                if not author:
                    author = crud_poetry.create_author(db=db, author={"name": name, "introduce": introduce})
                author_id = author.id
                poetry = crud_poetry.get_poetry_by_name_and_author_id(db, poetry_name, author_id)
                if not poetry:
                    poetry = crud_poetry.create_poetry(db, poetry={
                        "type": tstr,
                        "phrase": phrase,
                        "explain": explain,
                        "name": poetry_name,
                        "appreciation": appreciation,
                        "original": original,
                        "translation": translation,
                        "url": details_link,
                        "author_id": author_id,
                    })
                    logger.info(f"古诗：{poetry_name} 爬取成功！作者：{name}")
                    result["result"] += poetry_name + "\n"
    return result
