import requests
import time
from datetime import date
from jsonpath import jsonpath
from random import randint

from conf.settings import GAO_KEY, CITY_CODE, IDIOM_KEY


def get_weather():
    params = {
        "key": f"{GAO_KEY}",
        "city": f"{CITY_CODE}",
        "extensions": "base",
        "output": "JSON",
    }
    res = requests.get("https://restapi.amap.com/v3/weather/weatherInfo", params=params, verify=False)
    res.encoding = "utf-8"
    weather = jsonpath(res.json(), "$.lives[*].weather")
    return weather[0] if weather else ""


def now_season():
    season = ""
    month = date.today().month
    if month in [3, 4, 5]:
        season = ["春天", "清明节", "寒食节"]
    elif month in [6, 7, 8]:
        season = ["夏天", "七夕节", "端午节"]
    elif month in [9, 10, 11]:
        season = ["秋天", "中秋节", "重阳节"]
    elif month in [12, 1, 2]:
        season = ["冬天", "元宵节", "春节"]
    return season


def recommend_handle():
    weather = get_weather()
    if "晴" in weather:
        type_list = ["西湖", "爱情", "友情", "抒情"]
    elif "雨" in weather:
        type_list = ["写雨", "思乡", "离别", "伤感", "送别"]
    elif "风" in weather:
        type_list = ["写风", "柳树", "桃花", "菊花", "忧民"]
    elif "雪" in weather:
        type_list = ["写雪", "梅花"]
    elif "阴" in weather:
        type_list = ["小窗幽记", "闺怨", "怀古"]
    elif "云" in weather:
        type_list = ["星星", "月亮", "写云"]
    elif "雾" in weather:
        type_list = ["田园", "泰山", "庐山"]
    elif "沙" in weather:
        type_list = ["感恩", "哲理", "边塞"]
    else:
        type_list = ["史记", "国语", "吕氏春秋", "贞观政要", "围炉夜话"]
    type_list.extend(now_season())
    poetry_type = type_list[randint(0, len(type_list) - 1)]
    return poetry_type


def surplus_second():
    today = date.today()
    today_end = f"{str(today)} 23:59:59"
    end_second = int(time.mktime(time.strptime(today_end, "%Y-%m-%d %H:%M:%S")))
    now_second = int(time.time())
    return end_second - now_second


def idiom_solitaire(text: str):
    url = "http://apis.juhe.cn/idiomJie/query"
    params = {
        "key": IDIOM_KEY,
        "wd": text,
        "size": 10,
        "is_rand": 1,  # 是否随机返回结果，1:是 2:否。默认2
    }
    res = requests.get(url, params=params, verify=False).json()
    data_list = res["result"]["data"]
    last_word = res["result"]["last_word"]
    content = "成语接龙开始咯！\n"
    if not data_list:
        content += f"emmm，结束了嘿，么有找到 {last_word} 开头的成语。"
        return content
    content += f'最后一个字：{last_word}\n'
    for data in res["result"]["data"]:
        content += f"<a href='weixin://bizmsgmenu?msgmenucontent={data}&msgmenuid=9523'>{data}</a>\n"
    content += ">>> 点击成语"
    return content


if __name__ == '__main__':
    print(recommend_handle())
