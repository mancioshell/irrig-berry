#!/bin/bash
export PLATFORM=raspberry
gunicorn -k gevent --bind 0.0.0.0:5000 wsgi --daemon
