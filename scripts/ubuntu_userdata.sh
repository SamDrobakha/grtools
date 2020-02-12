#!/bin/bash

echo "_______________________________"
echo "updating instance"
echo "_______________________________"
sleep 1
apt update
apt install -y apt-transport-https ca-certificates vim htop net-tools git awscli build-essential python-pip python3-pip curl gnupg gnupg-agent libcurl4 traceroute nmap


echo "_______________________________"
echo "installing docker"
echo "_______________________________"
sleep 1
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - && add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt update 
apt install -y docker-ce docker-ce-cli containerd.io
username=ubuntu # !!! ADD YOUR USERNAME HERE !!!
#groupadd docker
#newgrp docker
usermod -aG docker $username
docker run hello-world


echo "_______________________________"
echo "installing docker-compose"
echo "_______________________________"
sleep 1
curl -L "https://github.com/docker/compose/releases/download/1.25.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose && docker-compose --version


echo "_______________________________"
echo "done"
echo "_______________________________"
exit 0
