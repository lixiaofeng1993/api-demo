import requests
from datetime import date


def now_season():
    season = ""
    month = date.today().month
    if month in [3, 4, 5]:
        season = "春天"
    elif month in [6, 7, 8]:
        season = "夏天"
    elif month in [9, 10, 11]:
        season = "秋天"
    elif month in [12, 1, 2]:
        season = "冬天"
    return season


def get_weather():
    res = requests.get("http://www.weather.com.cn/data/cityinfo/101010400.html")
    res.encoding = "utf-8"
    return res.json()["weatherinfo"]["weather"]


if __name__ == '__main__':
    get_weather()
