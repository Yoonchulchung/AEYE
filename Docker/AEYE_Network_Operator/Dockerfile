#############################################################
# AEYE AI Network Operator DockerFile
# Created By Yoonchul Chung
# Created At 2024.08.03
# Welcome to Visit Github : https://github.com/Yoonchulchung
#############################################################

FROM python:3.8-slim


#############################################################
# Install Dependencies
WORKDIR /app
COPY /Docker/AEYE_Network_Operator/dependencies.txt /app/

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
WORKDIR /app/

COPY /AEYE_Network_Operator/ /app/

#############################################################
# Result


EXPOSE 3000

CMD ["python", "manage.py", "runserver", "0.0.0.0:3000"]
