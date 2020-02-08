#!/usr/bin/env bash

echo "bash"

echo "running migrations"

# mysql -u root -p "jenish1"
sleep 25

if [ ! -d "migrations" ];then
    echo "no folder"
    flask db init
fi

flask db migrate
flask db upgrade

flask run --host=0.0.0.0


