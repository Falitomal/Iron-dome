#!/bin/bash
echo "Waiting for the containers to start..."
docker-compose up -d
echo "IronDome is up and running!"
echo "Inspect the network and list the running containers... "
docker container ls
echo "Network inspect..."
docker network inspect irondome | grep -e MacAddress -e Name -e IPv4
echo "Connect to SSH:\n ssh -p 4243 iron@localhost \n password: iron"