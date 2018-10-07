FROM python:3-alpine

ADD . /app
COPY . /app
WORKDIR /app

RUN pip install requests
RUN pip install gunicorn
RUN pip install -r requirements.txt

ARG DEVELOPMENT=True
ARG FLASK_ENV=development
ARG FLASK_APP=/server/app.py
CMD gunicorn --pythonpath app app.server.app:app


