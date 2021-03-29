#!/bin/bash

# docker-compose -f dockerfiles/docker-compose.blue.yml -p blue up --build -d 
# docker-compose -f dockerfiles/docker-compose.green.yml -p green  up --build -d

echo "-->deploy.sh<--"
echo "start deploy process at: ${PWD}"

EXIST_BLUE=$(docker-compose -p blue -f dockerfiles/docker-compose.blue.yml ps | grep Up)

if [ -z "$EXIST_BLUE" ]; then
	echo "blue up"
	docker-compose -f dockerfiles/docker-compose.blue.yml -p blue up --build -d
	sleep 10
	# TODO: if blue up, send slack to deploy success and green down
	# TODO: else blue no up, send slack to deploy fails and send logs
	docker-compose -f dockerfiles/docker-compose.green.yml -p green down
else
	echo "green up"
	docker-compose -f dockerfiles/docker-compose.green.yml -p green up --build -d
	sleep 10
	# TODO
	docker-compose -f dockerfiles/docker-compose.blue.yml -p blue down
fi
