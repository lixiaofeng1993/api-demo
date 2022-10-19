#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: settings.py
# 说   明: 
# 创建时间: 2021/12/26 23:30
# @Version：V 0.1
# @desc :

import platform
import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# 线上环境 False / True
DEBUG = True if platform.system() == "Windows" else False

HOST = "http://127.0.0.1:8000" if platform.system() == "Windows" else "http://121.41.54.234"
ASSETS_PATH = os.path.join(BASE_PATH, "media")

# 微信公众号
TOKEN = "lixiaofeng"
AppID = "wx99e27a845c7d8c52"
AppSecret = "fff1120327c7297e536c44979a6273d3"

FOLLOW = "这世界怎么那么多人，蹉跎回首，已不再年轻。\n这世界怎么那么多人，兜兜转转，浑噩半生。\n这世界怎么那么多人......\n\n" \
         "回复 <a href='weixin://bizmsgmenu?msgmenucontent=李白&msgmenuid=李白'>诗人</a> >>> 诗人简介\n" \
         "回复 <a href='weixin://bizmsgmenu?msgmenucontent=蜀道难&msgmenuid=蜀道难'>诗名</a> >>> 古诗信息\n" \
         "回复股票 <a href='weixin://bizmsgmenu?msgmenucontent=西部黄金&msgmenuid=西部黄金'>名称</a> " \
         "<a href='weixin://bizmsgmenu?msgmenucontent=601069&msgmenuid=601069'>代码</a> >>> 股票走势信息\n"
# "回复 【<a href='weixin://bizmsgmenu?msgmenucontent=1993.05.16&msgmenuid=1993.05.16'>1993.05.16</a>】，" \
#          "返回已经走过的天数信息\n" \
# "回复 【<a href='weixin://bizmsgmenu?msgmenucontent=小七&msgmenuid=小七'>小七</a>】，返回小七美照\n" \
# "回复 【<a href='weixin://bizmsgmenu?msgmenucontent=today&msgmenuid=today'>today</a>】，返回万年历当天信息\n" \
# "回复 【<a href='weixin://bizmsgmenu?msgmenucontent=放假&msgmenuid=放假'>放假</a>】，返回万年历当年放假安排\n" \
# "回复 【<a href='weixin://bizmsgmenu?msgmenucontent=follow&msgmenuid=follow'>功能</a>】，返回公众号功能信息\n"
ArticleUrl = "<a href='https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3NDg2Njc3MQ==&action=getalbum&album_id=" \
             "2622547569440768001#wechat_redirect'>点击查看所有文章</a>"

# 古诗词
# 朝代
DYNASTY = {
    "先秦": 4, "两汉": 10, "魏晋": 10, "南北朝": 10, "隋代": 5, "唐代": 10, "五代": 7, "宋代": 10, "金朝": 10, "元代": 10,
    "明代": 10, "清代": 10
}
# 诗词类型页数
POETRY_TYPE = {
    '春天': 9, '夏天': 2, '秋天': 7, '冬天': 4, '爱国': 6, '写雪': 4, '思念': 10, '爱情': 10, '思乡': 7,
    '离别': 9, '月亮': 5, '梅花': 4, '励志': 9, '荷花': 2, '写雨': 5, '友情': 7, '感恩': 3,
    '写风': 4, '西湖': 2, '读书': 3, '菊花': 3, '长江': 2, '黄河': 2, '竹子': 2, '哲理': 10, '泰山': 1,
    '边塞': 5, '柳树': 4, '写鸟': 9, '桃花': 2, '老师': 1, '母亲': 2, '伤感': 10, '田园': 3,
    '写云': 2, '庐山': 2, '山水': 8, '星星': 2, '荀子': 5, '孟子': 4, '论语': 4,
    '墨子': 3, '老子': 3, '史记': 3, '中庸': 2, '礼记': 2, '尚书': 3, '晋书': 1, '左传': 2, '论衡': 1, '管子': 2,
    '说苑': 2, '列子': 1, '国语': 1, '节日': 6, '春节': 2, '元宵节': 2, '寒食节': 1, '清明节': 2, '端午节': 1, '七夕节': 3,
    '中秋节': 2, '重阳节': 1, '韩非子': 4, '菜根谭': 2, '红楼梦': 3, '弟子规': 2, '战国策': 2, '后汉书': 2, '淮南子': 2, '商君书': 2,
    '水浒传': 2, '格言联璧': 5, '围炉夜话': 4, '增广贤文': 5, '吕氏春秋': 2, '文心雕龙': 2, '醒世恒言': 2,
    '警世通言': 2, '幼学琼林': 2, '小窗幽记': 3, '三国演义': 2, '贞观政要': 2
}
