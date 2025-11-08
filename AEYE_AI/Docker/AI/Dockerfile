

FROM pytorch/pytorch:2.7.1-cuda11.8-cudnn9-runtime

WORKDIR /app/

RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    libgl1-mesa-glx \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY ../app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download en_core_web_sm

