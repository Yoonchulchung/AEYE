#!/bin/bash

RED='\033[38;5;196m'
GREEN='\033[38;5;82m'
YELLOW='\033[38;5;226m'
BLUE='\033[38;5;81m'
NC='\033[0m' # No Color (Defualt colour)

##################################################################
install_status_VAR=1

total_progress=3

print_AEYE_AI() {
  clear
  figlet Welcome To
  figlet AEYE AI 
}

initialize_system() {
  clear
  echo "Updating system package list..."
  sudo apt update
  sudo apt install -y
  
  if [ $? -eq 0 ]; then
    install_status_VAR=0
    echo "System package list updated successfully."
    echo -e "${BLUE}[0/$total_progress] ${NC}Install figlet..."
    sudo apt install figlet -y
    
    if [ $? -eq 0 ]; then
      clear
      print_AEYE_AI
    else
      install_status_VAR=1
      echo -e "${RED}[0/$total_progress] Failed to install." ${NC}
    fi
    
  else
    echo ${RED}"Failed to update system package list."${NC}
  fi
}

initialize_system

########################################################################
install_dependencies () {
  sudo pip install -r dependencies_AI.txt
  
  if [ $? -eq 0 ]; then
    echo -e "${BLUE}[1/$total_progress] ${NC}Dependencies are installed successfully."  
  else
    install_status_VAR=1
    echo -e "${RED}[1/$total_progress] Failed to install." ${NC}
  fi
}

intialize_docker_install () {
  sudo apt install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
  
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg -y --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
  
  echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  
  if [ $? -eq 0 ]; then
    echo -e "${BLUE}[2/$total_progress] ${NC}Docker install initialization Succeed."
  else
    install_status_VAR=1
    echo -e "${RED}[2/$total_progress] ${NC}Dokcer install initialization Failed."
  fi
}

install_docker () {
  intialize_docker_install
  
  sudo apt update
  if [ $? -eq 0 ]; then
    sudo apt install -y docker-ce docker-ce-cli containerd.io
    
    # Create the docker group.
    sudo groupadd docker
  else
    install_status_VAR=1
    echo -e "${RED}[2/3] ${NC}Failed to install docker"
  fi
  
}

install_nvidia_docker() {
  distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
    && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
    && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
   
  sudo apt update
  sudo apt install -y nvidia-docker2

  sudo systemctl restart docker

  sudo docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi

}

install() {
  if [ $install_status_VAR -eq 0 ]; then
    echo -e "${BLUE}[1/$total_progress] ${NC}Install dependencies..."
    install_dependencies
  else
    echo -e "${RED}[1/$total_progress] ${NC}Failed to install dependencies due to install_status_VAR = 1."
  fi
  
  if [ $install_status_VAR -eq 0 ]; then
    echo -e "${BLUE}[2/$total_progress] ${NC}Install Docker..."
    figlet Install Docker
    install_docker 
  else
    echo -e "${RED}[2/$total_progress] ${NC}Failed to install Docker due to install_status_VAR = 1"
  fi
    
  if [ $install_status_VAR -eq 0 ]; then
    echo -e "${BLUE}[3/$total_progress] ${NC}Install Nvidia Doocker...."
    figlet Install 
    figlet Nvidia Docker
    install_nvidia_docker
  else
    echo -e "${RED}[3/$total_progress] ${NC}Failed to install Nvidia Docker due to install_status_VAR = 1"
  fi
}

install

# run server
#figlet Start Server
#cd AEYE_AI_Back_3_2
#python manage.py runserver



