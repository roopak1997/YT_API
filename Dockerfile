# base image
FROM python:3.7

RUN mkdir -p /app
WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

ADD . $DOCKERHOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
