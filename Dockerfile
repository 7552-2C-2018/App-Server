FROM python:3-alpine

ADD . /app
COPY . /app
WORKDIR /app
RUN apk add --update make gcc libc-dev libjpeg-turbo-dev
RUN pip install -r requirements.txt
RUN pip install requests
RUN pip install gunicorn


ENV MONGO_URI = mongodb://admin:Taller2018@ds245532.mlab.com:45532/app-server

CMD gunicorn --pythonpath app app.server.app:app


