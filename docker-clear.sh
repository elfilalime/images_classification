#!/bin/bash

# Delete all containers
docker rm $(docker ps -a -q)

# Delete all images
docker rmi $(docker images -q)

# Delete all volumes
docker volume rm $(docker volume ls -q)

# Delete all networks
# TODO docker network rm c520032c3d31

# Delete everything
# docker system prune --volumes