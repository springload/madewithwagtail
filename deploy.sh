#!/bin/sh -e

cd $(dirname $(echo $0))

python manage.py collectstatic --no-input
python manage.py createcachetable
python manage.py migrate --no-input
