#!/usr/bin/env bash

git pull

docker tag oddsserver-web:latest oddsserver-web:old
docker tag oddsserver-beat:latest oddsserver-beat:old
docker tag oddsserver-celery:latest oddsserver-celery:old

docker compose pull --quiet
docker compose build
docker compose down -v
docker compose up --detach

docker image rm oddsserver-web:old
docker image rm oddsserver-beat:old
docker image rm oddsserver-celery:old

docker image ls