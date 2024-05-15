#!/bin/bash

spin='-\|/'
i=0

# Start database and domserver
docker-compose -f compose-server.yaml up -d

# Wait for domserver to deploy
# while [[ $(docker-compose ps -q domserver-8.2.4) == "" ]]; do
echo "Deploying containers..."
while [[ ! i -eq 50 ]]; do
	printf "\r${spin:$((i%4)):1}"
	sleep 0.5
	((i++))
done

echo "Server created succesfully"

# Obtain the password used for judgehost creation
PASSWORD=$(docker exec domserver-8.2.4 cat /opt/domjudge/domserver/etc/restapi.secret | awk 'END {print $4}')
export JUDGEDAEMON_PASSWORD=$PASSWORD

echo "Password obtained succesfully"

# Start the judgehost container
docker-compose -f compose-judgehost.yaml up -d

echo "Your administrator credentials are:"
echo "User: admin"
PASSWORD=$(docker exec -it domserver-8.2.4 cat /opt/domjudge/domserver/etc/initial_admin_password.secret)
echo "Password: $PASSWORD"