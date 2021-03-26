#!/bin/bash

# docker-compose -f dockerfiles/docker-compose.blue.yml -p blue up --build -d 
# docker-compose -f dockerfiles/docker-compose.green.yml -p green  up --build -d

echo "-->deploy.sh<--"
echo "start deploy process at: ${PWD}"

EXIST_BLUE=$(docker-compose -p blue -f dockerfiles/docker-compose.blue.yml ps | grep Up)

if [ -z "$EXIST_BLUE" ]; then
	echo "blue up"
	docker-compose -f dockerfiles/docker-compose.blue.yml -p blue up -d
	sleep 10
	docker-compose -f dockerfiles/docker-compose.green.yml -p green down
else
	echo "green up"
	docker-compose -f dockerfiles/docker-compose.green.yml -p green up -d
	sleep 10
	docker-compose -f dockerfiles/docker-compose.blue.yml -p blue down
fi
