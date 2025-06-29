FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt /app/
COPY ./main.py /app/
COPY ./seed.py /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

