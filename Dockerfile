FROM python:3.10.5-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# RUN mkdir /code
WORKDIR /code
COPY requeriments.txt /code/

RUN pip install -r requeriments.txt

COPY . /code/
