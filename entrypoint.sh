#!/usr/bin/env sh
flask db init && flask db migrate -m "init" && flask db upgrade
flask run --host=0.0.0.0