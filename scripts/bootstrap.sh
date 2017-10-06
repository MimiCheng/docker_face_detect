#!/bin/bash

service ssh start

cd /home/face_demo/ && python3 app.py > /tmp/out.txt 2>&1
jupyter notebook --ip 0.0.0.0 --allow-root --no-browser > /mnt/token.txt 2>&1


if [[ $1 == "-d" ]]; then
  while true; do sleep 1000; done
fi

if [[ $1 == "-bash" ]]; then
  /bin/bash
fi
