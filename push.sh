#!/bin/bash

$(aws ecr get-login --no-include-email --region us-east-2)
docker build -t brighthive/honeybadger .
docker tag brighthive/honeybadger:latest 396527728813.dkr.ecr.us-east-2.amazonaws.com/brighthive/honeybadger:latest
docker push 396527728813.dkr.ecr.us-east-2.amazonaws.com/brighthive/honeybadger:latest