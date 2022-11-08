#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: scheduler.py
# 创建时间: 2022/11/8 0008 19:05
# @Version：V 0.1
# @desc :
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from public.stock_recommend import stock
from public.shares import shares

REDIS_DB = {
    "host": "127.0.0.1",
    "password": "123456"
}

interval_task = {
    # 配置存储器
    "jobstores": {
        # 使用Redis进行存储
        'default': RedisJobStore(**REDIS_DB)
    },
    # 配置执行器
    "executors": {
        # 使用进程池进行调度，最大进程数是10个
        'default': ProcessPoolExecutor(10)
    },
    # 创建job时的默认参数
    "job_defaults": {
        'coalesce': False,  # 是否合并执行
        'max_instances': 3,  # 最大实例数
    }

}
scheduler = AsyncIOScheduler(**interval_task)
# 添加一个定时任务
scheduler.add_job(stock, trigger='cron', hour="9-21", minute="*", args=[True], id="stock_job", replace_existing=True)
scheduler.add_job(shares, trigger='interval', seconds=30, id="shares_job", replace_existing=True)
