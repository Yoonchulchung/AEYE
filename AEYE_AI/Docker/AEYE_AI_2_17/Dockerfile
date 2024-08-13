#############################################################
# AEYE AI OpticNet Tensorflow Version 2.17 DockerFile
# Created By Yoonchul Chung
# Created At 2024.08.11
# Welcome to Visit Github : https://github.com/Yoonchulchung
#############################################################

FROM tensorflow/tensorflow:2.17.0-gpu


#############################################################
# Install Dependencies

RUN pip install pycm==1.9 matplotlib sklearn

RUN pip install --upgrade pip
RUN pip install opencv-python
RUN pip install Flask==1.1.4
RUN pip install colorama

RUN apt-get update
RUN apt-get install -y libgl1-mesa-glx --fix-missing

#############################################################
# Copy Files
WORKDIR /app/AEYE_AI
COPY /AEYE_AI/ /app/AEYE_AI/

COPY /Docker/AEYE_AI/dependencies.txt /app/AEYE_AI
RUN pip install -r dependencies.txt

#############################################################
# Set Environment

ENV PYTHONPATH "${PYTHONPATH}:/app"

#############################################################
# Cleaning

#############################################################
# RUN
EXPOSE 6006
EXPOSE 2000
EXPOSE 8888
# CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=5000", "--no-browser", "--allow-root"]

CMD ["python", "manage.py"]

