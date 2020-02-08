#!/bin/bash

if [ ! -d "migrations" ];then
    flask db init
fi
flask db migrate
flask db upgrade

flask run --host=0.0.0.0


