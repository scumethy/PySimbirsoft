FROM python:3

ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /app
COPY requirements.txt /app/

RUN pip install -r requirements.txt -i https://pypi.douban.com/simple

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

CMD /wait && uvicorn src.api.asgi:app --reload --host 0.0.0.0 --port 8888

COPY . /app