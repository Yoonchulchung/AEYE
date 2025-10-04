#############################################################
# AEYE Web Docker Compose Starter
# Created By Yoonchul Chung
# Created At 2024.08.03
# Welcome to Visit Github : https://github.com/Yoonchulchung
#############################################################

initiate_docker_compose()
{
  clear
  figlet WELOCME TO 
  figlet AEYE WEB
  cd ../Docker/ && docker-compose up 2>&1 | tee docker-compose.log
}

npm_install()
{
  cd ../AEYE_Front && npm install
}

run()
{
  npm_install

  initiate_docker_compose
}

run


