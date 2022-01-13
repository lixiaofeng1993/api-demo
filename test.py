#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: test.py
# 说   明: 
# 创建时间: 2021/12/30 23:01
# @Version：V 0.1
# @desc :
from datetime import datetime, time, timedelta
from typing import Optional
from uuid import UUID
import uvicorn

from fastapi import Body, FastAPI

app = FastAPI()


@app.put("/items/{item_id}")
async def read_items(
        item_id: UUID,
        start_datetime: Optional[datetime] = Body(None),
        end_datetime: Optional[datetime] = Body(None),
        repeat_at: Optional[time] = Body(None),
        process_after: Optional[timedelta] = Body(None),
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }


if __name__ == '__main__':
    uvicorn.run(app="test:app", host="0.0.0.0", port=8000, reload=True, debug=True)
