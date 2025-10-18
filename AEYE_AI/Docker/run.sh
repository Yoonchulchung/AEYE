#############################################################
# AEYE Docker Compose Starter
# Created By Yoonchul Chung
# Created At 2024.08.03
# Welcome to Visit Github : https://github.com/Yoonchulchung
#############################################################

initiate_docker_compose()
{
  clear
  figlet WELOCME TO 
  figlet AEYE AI
  docker-compose up 2>&1 | tee docker-compose.log
}

initiate_docker_compose
