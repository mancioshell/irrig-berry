#!/bin/bash
export PLATFORM=local
gunicorn -k gevent --bind 0.0.0.0:5000 wsgi
