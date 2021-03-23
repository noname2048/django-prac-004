#!/bin/bash

# docker-compose -p gunicorn-app-blue -f dockerfiles/docker-compose.blue.yml up --build -d
# docker-compose -p gunicorn-app-green -f dockerfiles/docker-compose.green.yml up --build -d
echo "-->deploy.sh"
echo ${PWD}

DOCKER_APP_NAME=gunicorn-app
EXIST_BLUE=$(docker-compose -p ${DOCKER_APP_NAME}-blue -f dockerfiles/docker-compose.blue.yml ps | grep Up)

if [ -z "$EXIST_BLUE" ]; then
	echo "blue up"
	docker-compose -p ${DOCKER_APP_NAME}-blue -f dockerfiles/docker-compose.blue.yml up -d

	sleep 10

	docker-compose -p ${DOCKER_APP_NAME}-green -f dockerfiles/docker-compose.green.yml down
else
	echo "green up"
	docker-compose -p ${DOCKER_APP_NAME}-green -f dockerfiles/docker-compose.green.yml up -d

	sleep 10

	docker-compose -p ${DOCKER_APP_NAME}-blue -f dockerfiles/docker-compose.blue.yml down
fi
