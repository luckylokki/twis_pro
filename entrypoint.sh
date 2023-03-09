#!/usr/bin/env sh
flask db init && flask db migrate -m "init" && flask db upgrade
python app.py
