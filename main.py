from fastapi import FastAPI, Depends
from aioredis import Redis
import uvicorn
import aioredis

from api import users, project, sign
from dependencies import get_current_user

app = FastAPI()

data = {
    400: {
        "message": "返回错误"
    }
}


async def get_redis_pool() -> Redis:
    redis = await aioredis.from_url(f"redis://:@127.0.0.1:6379/0")
    return redis


@app.on_event("startup")
async def startup_event():
    app.state.redis = await get_redis_pool()


@app.on_event("shutdown")
async def shutdown_event():
    app.state.redis.close()
    await app.state.redis.wait_closed()


app.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_current_active_user)],
    responses=data
)

app.include_router(
    project.router,
    prefix="/project",
    tags=["project"],
    dependencies=[Depends(get_current_user)],
    responses=data
)

app.include_router(
    sign.router,
    prefix="/sign",
    tags=["sign"],
    dependencies=[Depends(get_current_user)],
    responses=data
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


if __name__ == '__main__':
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True, debug=True)
