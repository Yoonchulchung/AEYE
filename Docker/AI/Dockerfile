FROM pytorch/pytorch:2.7.0-cuda12.8-cudnn9-runtime

WORKDIR /app

COPY ../AEYE_AI/app /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
 && rm -rf /var/lib/apt/lists/*
 
RUN pip install --no-cache -r requirements.txt

EXPOSE 6000