FROM python:3.7

WORKDIR /root/apps/api-demo

RUN pip install --no-cache-dir uvicorn gunicorn

RUN pip install --no-cache-dir --upgrade -r requirements.txt -i https://pypi.douban.com/simple/

EXPOSE 8000

CMD ["gunicorn", "-c", "/root/apps/api-demo/gunicorn.py", "main:app", "-k", "uvicorn.workers.UvicornWorker"]