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
from faker import Faker
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
faker = Faker()


def not_empty(s):
    return s and s.strip()


@router.get("/author", summary="爬取作者信息接口")
async def get_author(db: Session = Depends(get_db), user: User = Depends(get_current_user_info)):
    author = crud_poetry.get_author_by_name(db, "佚名")
    if not author:
        crud_poetry.create_author(db, {
            "name": "佚名",
            "dynasty": "",
            "introduce": "亦称无名氏，是指身份不明或者尚未了解姓名的人。源于古代或民间、不知由谁创作的文学、音乐作品会以佚名为作者名称。",
        })
    dynasty_dict = {"先秦": 4, "两汉": 10, "魏晋": 10, "南北朝": 10, "隋代": 5, "唐代": 10, "五代": 7, "宋代": 10, "金朝": 10, "元代": 10,
                    "明代": 10, "清代": 10}
    for key, value in dynasty_dict.items():
        for i in range(1, value + 1):
            url = f"https://so.gushiwen.cn/authors/Default.aspx?p={i}&c={key}"
            # url = f"https://so.gushiwen.cn/authors/Default.aspx?p={i}&c=唐代"
            # dynasty = "唐代"
            dynasty = key
            with HTMLSession() as session:
                headers = {
                    "user-agent": faker.user_agent()
                }
                res = session.get(url, headers=headers).html
            data = res.find("#leftZhankai > .sonspic > .cont", first=True)
            if data:
                all_data = data.text.split("下一页 上一页")[0].split("完善")
                for datas in all_data:
                    if datas:
                        name, introduce = "", ""
                        data_list = list(filter(not_empty, datas.split("\n")))
                        if len(data_list) == 3:
                            name = data_list[-2]
                            introduce = data_list[-1]
                        elif len(data_list) == 2:
                            name = data_list[0]
                            introduce = data_list[1]
                        if name and introduce and dynasty:
                            author = crud_poetry.get_author_by_name_and_dynasty(db, name, dynasty)
                            if not author:
                                crud_poetry.create_author(db, {
                                    "name": name,
                                    "dynasty": dynasty,
                                    "introduce": introduce,
                                })
                                status = "保存成功！"
                            else:
                                status = ""
                            logger.info(f"第{i}页 {name} {dynasty} ==> {status}")
    return result


@router.get("/poetry", summary="爬取古诗词接口")
async def get_poetry(db: Session = Depends(get_db), user: User = Depends(get_current_user_info)):
    type_dict = {'春天': 9, '夏天': 2, '秋天': 7, '冬天': 4, '爱国': 6, '写雪': 4,
                 '思念': 10, '爱情': 10, '思乡': 7, '离别': 9, '月亮': 5, '梅花': 4, '励志': 9, '荷花': 2, '写雨': 5, '友情': 7, '感恩': 3,
                 '写风': 4, '西湖': 2, '读书': 3, '菊花': 3, '长江': 2, '黄河': 2, '竹子': 2, '哲理': 10, '泰山': 1,
                 '边塞': 5, '柳树': 4, '写鸟': 9, '桃花': 2, '老师': 1, '母亲': 2, '伤感': 10, '田园': 3,
                 '写云': 2, '庐山': 2, '山水': 8, '星星': 2, '荀子': 5, '孟子': 4, '论语': 4,
                 '墨子': 3, '老子': 3, '史记': 3, '中庸': 2, '礼记': 2, '尚书': 3, '晋书': 1, '左传': 2, '论衡': 1, '管子': 2,
                 '说苑': 2, '列子': 1, '国语': 1, '节日': 6, '春节': 2, '元宵节': 2, '寒食节': 1, '清明节': 2, '端午节': 1, '七夕节': 3,
                 '中秋节': 2, '重阳节': 1, '韩非子': 4, '菜根谭': 2, '红楼梦': 3, '弟子规': 2, '战国策': 2, '后汉书': 2, '淮南子': 2, '商君书': 2,
                 '水浒传': 2, '格言联璧': 5, '围炉夜话': 4, '增广贤文': 5, '吕氏春秋': 2, '文心雕龙': 2, '醒世恒言': 2,
                 '警世通言': 2, '幼学琼林': 2, '小窗幽记': 3, '三国演义': 2, '贞观政要': 2}
    type_dict = {
        '冬天': 4, '三国演义': 2, '柳树': 4, '贞观政要': 2, '春天': 9, '夏天': 2, '秋天': 7,
    }
    type_dict = {
    
    }
    for key, value in type_dict.items():
        for i in range(1, value + 1):
            url = f"https://so.gushiwen.cn/mingjus/default.aspx?page={i}&tstr={key}&astr=&cstr=&xstr="
            # url = f"https://so.gushiwen.cn/mingjus/default.aspx?page={i}&tstr=菜根谭&astr=&cstr=&xstr="
            poetry_type = key
            # poetry_type = "菜根谭"
            with HTMLSession() as session:
                headers = {
                    "user-agent": faker.user_agent()
                }
                res = session.get(url, headers=headers).html
            css_patt = ".sons > .cont"
            data = res.find(css_patt, first=True)
            if not data:
                logger.error(f"第一层 地址：{url} 没有发现 {css_patt}！！！")
                continue
            links = data.links
            details_links = []
            for link in links:
                if "/mingju/juv_" in link:
                    link = "https://so.gushiwen.cn" + link
                    details_links.append(link)
            j = 0
            poetry_list = []
            for link in details_links:
                with HTMLSession() as session:
                    headers = {
                        "user-agent": faker.user_agent()
                    }
                    detail_res = session.get(link, headers=headers).html
                j += 1
                detail_data = detail_res.find(css_patt, first=True)
                if not detail_data:
                    logger.error(f"第二层 地址：{url}, 未发现 {css_patt}")
                    continue
                logger.info(f"当前执行的url：{link}")
                detail = detail_data.text.split("猜您喜欢")[0]
                explain, appreciation, poetry_name, original, translation, background, name, dynasty = \
                    "", "", "", "", "", "", "", ""
                phrase_patt = "([\\s\\S]*?)完善"
                phrase_str = re.search(phrase_patt, detail).group()
                phrase_list = phrase_str.split("\n")
                if "document" in phrase_list[0]:
                    phrase_list = phrase_list[1:]
                phrase = phrase_list[0]  # 名句
                for text in phrase_list[1:]:
                    if "解释" in text:
                        explain = text.split("：")[-1]  # 解释
                    elif "赏析" in text:
                        appreciation = text.split("：")[-1]  # 赏析
                    elif "摘自" in text:
                        poetry_name_patt = "《(.+)》"
                        poetry_name = re.findall(poetry_name_patt, text)[0]  # 古诗名字
                    elif "出自" in text and "（出自" not in text:
                        name_patt = "[秦|汉|晋|朝|代](.+?)的《"
                        name = re.findall(name_patt, text)[0]  # 作者名字
                        if "(" in name and ")" in name:
                            _name_patt = "(.+)\\("
                            _name = re.findall(_name_patt, name)[0]
                            name = _name
                        dynasty_patt = f"出自(.+[秦|汉|晋|朝|代]){name}"
                        dynasty = re.findall(dynasty_patt, text)[0]  # 作者朝代
                        poetry_name_patt = "《(.+)》"
                        poetry_name = re.findall(poetry_name_patt, text)[0]  # 古诗名字
                    elif text != "完善":
                        original += text + "\n"
                original_patt = "原文([\\s\\S]+?)译文"
                original_list = re.findall(original_patt, detail)
                if original_list:
                    original = original_list[0]  # 原文
                    poetry_name_patt = "《(.+)》"
                    poetry_name = re.findall(poetry_name_patt, original)[0]  # 古诗名字
                    name_patt = "(.+?)《"
                    name = re.findall(name_patt, original)[0]
                translation_patt = "译文\\s([\\s\\S]+?)\\s注释"
                translation_list = re.findall(translation_patt, detail)
                if translation_list:
                    translation = translation_list[0]  # 译文
                background_patt = "创作背景\\s([\\s\\S]+?)\\s[参考资料|本节内容]"
                background_list = re.findall(background_patt, detail)
                if background_list:
                    background = background_list[0]  # 创作背景
                logger.info(
                    f"第{i}页 ==> 第{j}条 ==>名句：{phrase} ==> 作者：{name} ==> 朝代：{dynasty} ==> 古诗名字：{poetry_name} ==> "
                    f"古诗类型：{poetry_type}")
                if name == "佚名":
                    author = crud_poetry.get_author_by_name(db, name)
                    author_id = author.id
                elif name and name != "佚名" and dynasty:
                    author = crud_poetry.get_author_by_name_and_dynasty(db, name, dynasty)
                    if author:
                        author_id = author.id
                    else:
                        introduce_patt = f"({name}（.+)\\s完善"
                        introduce_list = re.findall(introduce_patt, detail)
                        introduce = introduce_list[0] if introduce_list else ""
                        author = crud_poetry.create_author(db, {
                            "name": name,
                            "dynasty": dynasty,
                            "introduce": introduce,
                        })
                        author_id = author.id
                        logger.info(f"{name} {dynasty} 保存成功！")
                else:
                    author_id = None
                poetry = crud_poetry.get_poetry_by_type_and_name_and_author_and_phrase(db, poetry_type,
                                                                                       poetry_name,
                                                                                       author_id, phrase)
                if not poetry:
                    poetry_list.append(
                        {
                            "type": poetry_type,
                            "phrase": phrase,
                            "explain": explain,
                            "name": poetry_name,
                            "appreciation": appreciation,
                            "original": original,
                            "translation": translation,
                            "background": background,
                            "url": link,
                            "author_id": author_id,
                        }
                    )
            if poetry_list:
                crud_poetry.add_all_poetry(db, poetry_list)
                logger.info(f"批量保存成功！古诗类型：{poetry_type} ==> {len(poetry_list)} 条")
    return result
