FROM python:3.7

WORKDIR /root/apps/api-demo

RUN pip install --no-cache-dir uvicorn gunicorn aioredis==1.3.1 fastapi==0.71.0 PyMySQL==1.0.2 python-jose==3.3.0 python-multipart==0.0.5 SQLAlchemy==1.4.29 pycryptodome==3.14.1 bcrypt==3.2.2 requests==2.28.1 requests-html==0.10.0 -i https://pypi.douban.com/simple/

#RUN pip install --no-cache-dir --upgrade -r requirements.txt -i https://pypi.douban.com/simple/

EXPOSE 8000

#CMD ["gunicorn", "-c", "/root/apps/api-demo/gunicorn.py", "main:app", "-k", "uvicorn.workers.UvicornWorker"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0","--port", "8000"]