FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

COPY . .

RUN pip install -r requirements.txt -i https://pypi.douban.com/simple

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

CMD /wait && cd ./user_service && alembic upgrade head && cd .. && PYTHONPATH='.' python3 ./user_service/main.py