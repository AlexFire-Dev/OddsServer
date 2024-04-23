#!/usr/bin/env bash

python3 manage.py collectstatic --clear --skip-checks --noinput
python3 manage.py migrate
gunicorn BondStats.wsgi:application -w 1 -t 600 -b 0.0.0.0:220
