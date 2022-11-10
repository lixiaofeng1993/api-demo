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
         "回复 <a href='weixin://bizmsgmenu?msgmenucontent=唐寅&msgmenuid=唐寅'>诗人</a> >>> 诗人简介\n" \
         "回复 <a href='weixin://bizmsgmenu?msgmenucontent=桃花庵歌&msgmenuid=桃花庵歌'>诗名</a> >>> 古诗信息\n" \
         "回复 <a href='weixin://bizmsgmenu?msgmenucontent=成语接龙&msgmenuid=成语接龙'>接龙</a> >>> 成语接龙\n" \
         "回复股票 <a href='weixin://bizmsgmenu?msgmenucontent=西部黄金&msgmenuid=西部黄金'>名称</a> " \
         "<a href='weixin://bizmsgmenu?msgmenucontent=601069&msgmenuid=601069'>代码</a> >>> 股票走势\n"
# "回复 【<a href="weixin://bizmsgmenu?msgmenucontent=1993.05.16&msgmenuid=1993.05.16">1993.05.16</a>】，" \
#          "返回已经走过的天数信息\n" \
# "回复 【<a href="weixin://bizmsgmenu?msgmenucontent=小七&msgmenuid=小七">小七</a>】，返回小七美照\n" \
# "回复 【<a href="weixin://bizmsgmenu?msgmenucontent=today&msgmenuid=today">today</a>】，返回万年历当天信息\n" \
# "回复 【<a href="weixin://bizmsgmenu?msgmenucontent=放假&msgmenuid=放假">放假</a>】，返回万年历当年放假安排\n" \
# "回复 【<a href="weixin://bizmsgmenu?msgmenucontent=follow&msgmenuid=follow">功能</a>】，返回公众号功能信息\n"
ArticleUrl = "<a href='https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3NDg2Njc3MQ==&action=getalbum&album_id=" \
             "2622547569440768001#wechat_redirect'>点击查看所有文章</a>"

# 古诗词
# 朝代
DYNASTY = {
    "先秦": 1, "两汉": 2, "魏晋": 3, "南北朝": 4, "隋代": 5, "唐代": 6, "五代": 7, "宋代": 8, "金朝": 9, "元代": 10,
    "明代": 11, "清代": 12
}
DYNASTY_REPTILE = {
    "先秦": 4, "两汉": 10, "魏晋": 10, "南北朝": 10, "隋代": 5, "唐代": 10, "五代": 7, "宋代": 10, "金朝": 10, "元代": 10,
    "明代": 10, "清代": 10
}
# 诗词类型
POETRY_TYPE = {
    "春天": 1, "夏天": 2, "秋天": 3, "冬天": 4, "爱国": 5, "写雪": 6, "思念": 7, "爱情": 8, "思乡": 9,
    "离别": 10, "月亮": 11, "梅花": 12, "励志": 13, "荷花": 14, "写雨": 15, "友情": 16, "感恩": 17,
    "写风": 18, "西湖": 19, "读书": 20, "菊花": 21, "长江": 22, "黄河": 23, "竹子": 24, "哲理": 25, "泰山": 26,
    "边塞": 27, "柳树": 28, "写鸟": 29, "桃花": 30, "老师": 31, "母亲": 32, "伤感": 33, "田园": 34,
    "写云": 35, "庐山": 36, "山水": 37, "星星": 38, "荀子": 39, "孟子": 40, "论语": 41,
    "墨子": 42, "老子": 43, "史记": 44, "中庸": 45, "礼记": 46, "尚书": 47, "晋书": 48, "左传": 49, "论衡": 50, "管子": 51,
    "说苑": 52, "列子": 53, "国语": 54, "节日": 55, "春节": 56, "元宵节": 57, "寒食节": 58, "清明节": 59, "端午节": 60, "七夕节": 61,
    "中秋节": 62, "重阳节": 63, "韩非子": 64, "菜根谭": 65, "红楼梦": 66, "弟子规": 67, "战国策": 68, "后汉书": 69, "淮南子": 70, "商君书": 71,
    "水浒传": 72, "格言联璧": 73, "围炉夜话": 74, "增广贤文": 75, "吕氏春秋": 76, "文心雕龙": 77, "醒世恒言": 78,
    "警世通言": 79, "幼学琼林": 80, "小窗幽记": 81, "三国演义": 82, "贞观政要": 83, "唐诗三百首": 84, "古诗三百首": 85, "宋词三百首": 86,
    "小学古诗文": 87, "初中古诗文": 88, "高中古诗文": 89, "宋词精选": 90, "古诗十九首": 91, "诗经": 92, "楚辞": 93, "乐府诗集精选": 94,
    "写景": 95, "咏物": 96, "写花": 97, "写山": 98, "写水": 99, "儿童": 100, "写马": 101, "地名": 102, "怀古": 103, "抒情": 104,
    "送别": 105, "闺怨": 106, "悼亡": 107, "写人": 108, "战争": 109, "惜时": 110, "忧民": 111, "婉约": 112, "豪放": 113, "民谣": 114,
}
POETRY_TYPE_1 = {
    # "春天": 9, "夏天": 2, "秋天": 7, "冬天": 4, "爱国": 6, "写雪": 4, "思念": 10, "爱情": 10, "思乡": 7,
    # "离别": 9, "月亮": 5, "梅花": 4, "励志": 9, "荷花": 2, "写雨": 5, "友情": 7, "感恩": 3,
    # "写风": 4, "西湖": 2, "读书": 3, "菊花": 3, "长江": 2, "黄河": 2, "竹子": 2, "哲理": 10, "泰山": 1,
    # "边塞": 5, "柳树": 4, "写鸟": 9, "桃花": 2, "老师": 1, "母亲": 2, "伤感": 10, "田园": 3,
    # "写云": 2, "庐山": 2, "山水": 8, "星星": 2, "荀子": 5, "孟子": 4, "论语": 4,
    # "墨子": 3, "老子": 3, "史记": 3, "中庸": 2, "礼记": 2, "尚书": 3, "晋书": 1, "左传": 2, "论衡": 1, "管子": 2,
    # "说苑": 2, "列子": 1, "国语": 1, "节日": 6, "春节": 2, "元宵节": 2, "寒食节": 1, "清明节": 2, "端午节": 1, "七夕节": 3,
    # "中秋节": 2, "重阳节": 1, "韩非子": 4, "菜根谭": 2, "红楼梦": 3, "弟子规": 2, "战国策": 2, "后汉书": 2, "淮南子": 2, "商君书": 2,
    # "水浒传": 2, "格言联璧": 5, "围炉夜话": 4, "增广贤文": 5, "吕氏春秋": 2, "文心雕龙": 2, "醒世恒言": 2,
    # "警世通言": 2, "幼学琼林": 2, "小窗幽记": 3, "三国演义": 2, "贞观政要": 2
}
# 古诗类型网址
POETRY_URL = {
    # "唐诗三百首": "/tangshi.aspx", "古诗三百首": "/sanbai.aspx", "宋词三百首": "/songsan.aspx", "小学古诗文": "/xiaoxue.aspx",
    # "初中古诗文": "/chuzhong.aspx", "高中古诗文": "/gaozhong.aspx", "宋词精选": "/songci.aspx", "古诗十九首": "/shijiu.aspx",
    # "诗经": "/shijing.aspx", "楚辞": "/chuci.aspx", "乐府诗集精选": "/yuefu.aspx", "写景": "/xiejing.aspx",
    # "咏物": "/yongwu.aspx", "春天": "/chuntian.aspx", "夏天": "/xiatian.aspx", "秋天": "/qiutian.aspx",
    # "冬天": "/dongtian.aspx", "写雨": "/yu.aspx", "写雪": "/xue.aspx", "写风": "/feng.aspx", "写花": "/hua.aspx",
    # "梅花": "/meihua.aspx", "荷花": "/hehua.aspx", "菊花": "/juhua.aspx", "柳树": "/liushu.aspx", "月亮": "/yueliang.aspx",
    # "山水": "/shanshui.aspx", "写山": "/shan.aspx", "写水": "/shui.aspx", "长江": "/changjiang.aspx", "黄河": "/huanghe.aspx",
    # "儿童": "/ertong.aspx", "写鸟": "/niao.aspx", "写马": "/ma.aspx", "田园": "/tianyuan.aspx", "边塞": "/biansai.aspx",
    # "地名": "/diming.aspx", "节日": "/jieri.aspx", "春节": "/chunjie.aspx", "元宵节": "/yuanxiao.aspx", "寒食节": "/hanshi.aspx",
    # "清明节": "/qingming.aspx", "端午节": "/duanwu.aspx", "七夕节": "/qixi.aspx", "中秋节": "/zhongqiu.aspx",
    # "重阳节": "/chongyang.aspx", "怀古": "/huaigu.aspx", "抒情": "/shuqing.aspx", "爱国": "/aiguo.aspx", "离别": "/libie.aspx",
    # "送别": "/songbie.aspx", "思乡": "/sixiang.aspx", "思念": "/sinian.aspx", "爱情": "/aiqing.aspx",
    # "励志": "/lizhi.aspx", "哲理": "/zheli.aspx", "闺怨": "/guiyuan.aspx", "悼亡": "/daowang.aspx", "写人": "/xieren.aspx",
    # "老师": "/laoshi.aspx", "母亲": "/muqin.aspx", "友情": "/youqing.aspx", "战争": "/zhanzheng.aspx",
    # "读书": "/dushu.aspx", "惜时": "/xishi.aspx", "忧民": "/youguo.aspx", "婉约": "/wanyue.aspx", "豪放": "/haofang.aspx",
    # "民谣": "/minyao.aspx",
}

# 股票
SHARES = {
    "name": "股票名称",
    "code": "股票代码",
    "date_time": "日期",
    "open_price": "开盘",
    "new_price": "收盘",
    "top_price": "最高",
    "down_price": "最低",
    "turnover": "成交量",
    "business_volume": "成交额",
    "amplitude": "振幅",
    "rise_and_fall": "涨跌幅",
    "rise_and_price": "涨跌额",
    "turnover_rate": "换手率"
}
# 是否持仓
STOCK_FLAG = True
# 持仓股票
STOCK_NAME = "宝鹰股份"
# 持仓数量 股
BUY_NUM = 400
# 持仓成本 元
BUY_PRICE = 4.95
# 原始亏损 元
LOSS_PRICE = 0

# 万年历KEY
CALENDAR_KEY = "197557d5fc1f3a26fa772bc694ea4c2d"
# 万年历成语接龙
IDIOM_KEY = "3b46a1f367b46094fcb766e56f76170f"
# 成语大全
IDIOM_INFO = "2f8b9617804af8aaedbc264b37c116aa"
# 天气
WEATHER_KEY = "4dd0557f59831bd698f8bb4a830145c4"
# 高德地图KEY
GAO_KEY = "b5b15bbd3252eb0cbb01877ae53a34d7"
# 北京 110000
# 顺义 110113
# 屯留 140405
# 长治 140400
# 太原 140100
# 城市代码
CITY_CODE = 110113
# 城市名称
CITY_NAME = "北京"
