#!/usr/bin/env bash

echo "bash"

echo "running migrations"

# while ! nc -z db 3306; do
#   sleep 0.5
# done
sleep 15
if [ ! -d "migrations" ];then
    echo "no folder"
    flask db init
fi

flask db migrate
flask db upgrade

flask run --host=0.0.0.0


