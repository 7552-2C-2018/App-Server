FROM python:3-alpine

ADD . /app
WORKDIR /app

RUN pip install requests
RUN pip install gunicorn
RUN pip install -r requirements.txt

CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "server.app:app"