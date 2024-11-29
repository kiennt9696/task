#!/bin/bash

worker=${WORKER:-1}
port=${PORT:-8082}
timeout=${TIMEOUT:-30}

gunicorn -c prometheus_config.py --bind 0.0.0.0:${port} -k gevent -w $worker --timeout $timeout wsgi
