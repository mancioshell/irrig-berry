#!/bin/bash
export PLATFORM=$1
gunicorn -k gevent --bind 0.0.0.0:5000 wsgi -- daemon
