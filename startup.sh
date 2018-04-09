#!/bin/bash
cd waterberry
cd public && npm install
cd ../
pipenv install
pipenv shell
export FLASK_APP=app.py
flask run --host=0.0.0.0
