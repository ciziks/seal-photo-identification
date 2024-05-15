FROM python:3.11-buster

RUN mkdir app
WORKDIR /app

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=.

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY src/ .
COPY seal_schema.sql .

RUN apt update && apt install -y sqlite3

RUN sqlite3 sealcenter.db < seal_schema.sql
