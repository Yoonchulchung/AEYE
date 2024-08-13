#############################################################
# AEYE WEB Router DockerFile
# Created By Yoonchul Chung
# Created At 2024.08.07
# Welcome to Visit Github : https://github.com/Yoonchulchung
#############################################################

FROM python:3.8-slim


#############################################################
# Install Dependencies
WORKDIR /app
COPY /Docker/Network_Router/dependencies.txt /app/

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install -r dependencies.txt


#############################################################
# Clean

#############################################################
# Copy DIR
WORKDIR /app/AEYE_Router

COPY /AEYE_Router/ /app/AEYE_Router

#############################################################
# Result


EXPOSE 2000

CMD ["python", "manage.py", "runserver", "0.0.0.0:2000"]
