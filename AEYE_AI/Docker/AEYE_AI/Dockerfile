#############################################################
# AEYE AI OpticNet DockerFile
# Created By Yoonchul Chung
# Created At 2024.08.03
# Welcome to Visit Github : https://github.com/Yoonchulchung
#############################################################

FROM tensorflow/tensorflow:1.12.0-rc1-gpu-py3

WORKDIR /app/

COPY /Docker/AEYE_AI/dependencies.txt /app
RUN pip install --upgrade pip
RUN pip install -r dependencies.txt

RUN apt-get update & apt-get install -y libgl1-mesa-glx --fix-missing

ENV PYTHONPATH "${PYTHONPATH}:/app"

EXPOSE 5000

CMD ["python", "manage.py"]

