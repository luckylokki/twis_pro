#!/usr/bin/env sh
sleep 1
flask db init && flask db migrate -m "init" && flask db upgrade
flask run --host=0.0.0.0