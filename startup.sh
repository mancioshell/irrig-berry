#!/bin/bash
export PLATFORM=local
export FLASK_APP=app.py
export FLASK_DEBUG=1
cd waterberry
python -m flask run --host=0.0.0.0
