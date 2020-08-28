FROM python:3

ENV PYTHONUNBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /app
COPY requirements.txt /app/

RUN pip install -r requirements.txt -i https://pypi.python.org/simple

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

CMD /wait && alembic upgrade head && uvicorn api.asgi:app --reload --host 0.0.0.0 --port 8088

COPY . /app