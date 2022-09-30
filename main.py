import uvicorn
from fastapi import FastAPI, Depends
from aioredis import Redis, create_redis_pool

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
from pathlib import Path

from tasks import repeat_task
from public.shares import shares
from api import users, project, sign, api
from dependencies import get_current_user
from public.custom_code import response_error

app = FastAPI(title="EasyTest接口项目", description="这是一个接口文档", version="1.0.0", docs_url=None, redoc_url=None)

BASE_DIR = Path(__file__).resolve().parent

MEDIA_PATH = BASE_DIR / 'media'

app.mount('/static', StaticFiles(directory='static'), name='static')
app.mount(path="/media", app=StaticFiles(directory=MEDIA_PATH), name='media')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_redis_pool() -> Redis:
    redis = await create_redis_pool(f"redis://:@127.0.0.1:6379/0", encoding="utf-8")
    return redis


@app.on_event("startup")
async def startup_event():
    app.state.redis = await get_redis_pool()


@app.on_event('startup')
@repeat_task(seconds=60 * 1, wait_first=True)
def repeat_task_aggregate_request_records() -> None:
    shares()


@app.on_event("shutdown")
async def shutdown_event():
    app.state.redis.close()
    await app.state.redis.wait_closed()


app.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_current_active_user)],
    responses=response_error
)

app.include_router(
    project.router,
    prefix="/project",
    tags=["project"],
    dependencies=[Depends(get_current_user)],
    responses=response_error
)

app.include_router(
    sign.router,
    prefix="/sign",
    tags=["sign"],
    dependencies=[Depends(get_current_user)],
    responses=response_error
)

app.include_router(
    api.router,
    prefix="/api",
    tags=["api"],
    responses=response_error
)


@app.get("/")
async def root():
    from datetime import datetime
    return {
        "message": "儿砸，叫爸爸！！！",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "doc": "http://121.41.54.234/docs#/"
    }


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )


if __name__ == '__main__':
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True, debug=True)
