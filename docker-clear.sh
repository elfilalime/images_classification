#!/bin/bash

# Delete all containers
docker rm $(docker ps -a -q)

# Delete all images
docker rmi $(docker images -q)

# Delete all volumes
docker volume rm $(docker volume ls -q)

# Delete all networks
docker network rm $(docker network ls -q)

# Delete everything
# docker system prune --volumes