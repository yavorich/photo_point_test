FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /backend/

#RUN apt-get update -y && apt-get -y install locales-all

ADD backend .
ADD requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV LC_TIME ru_RU.UTF-8
