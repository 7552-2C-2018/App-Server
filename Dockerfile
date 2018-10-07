FROM python:3-alpine

ADD . /app
COPY . /app
WORKDIR /app

RUN pip install requests
RUN pip install gunicorn
RUN pip install -r requirements.txt

ENV MONGO_URI = mongodb://admin:Taller2018@ds245532.mlab.com:45532/app-server

CMD gunicorn --pythonpath app app.server.app:app


