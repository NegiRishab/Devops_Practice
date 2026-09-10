#!/usr/bin/env bash
cd /home/ec2-user

source /home/ec2-user/server.env
export BACKEND_IMAGE=$1
export FRONTEND_IMAGE=$2
docker compose -f docker-compose.yml pull
docker compose -f docker-compose.yml up -d
echo "compose up done"