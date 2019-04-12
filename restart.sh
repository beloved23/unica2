#!/bin/bash
#source ~/Envs/new/bin/activate
workon django10
pkill -f 'newunica.wsgi'

echo starting gunicorn
exec gunicorn newunica.wsgi -b 0.0.0.0:8090 \
     --workers=5 -t 2300 \
     --worker-connections 100



