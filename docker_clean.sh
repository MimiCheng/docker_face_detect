#!/bin/bash
docker rmi --force $(docker images | grep "^<none>" | awk '{print $3}')
docker rmi --force $(docker images -f "dangling=true" -q)
