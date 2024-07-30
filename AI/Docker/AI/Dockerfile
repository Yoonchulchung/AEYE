FROM tensorflow/tensorflow:1.12.0-gpu-py3 AS aeye_ai_1_0 

FROM aeye_ai_1_0 AS deps
WORKDIR /app
COPY dependencies_AI.txt /app/

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

FROM deps AS runner

COPY OpticNet-71-master/ * /app/ai


