#############################################################
# AEYE Web Backend Dockerfile
# Created By Yoonchul Chung
# Created At 2025.10.04
# Welcome to Visit Github : https://github.com/Yoonchulchung
#############################################################
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

COPY ../AEYE_Back/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY ../AEYE_Back/ /app/

EXPOSE 8000

CMD ["bash", "-c", "python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]
