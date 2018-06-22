#!/bin/bash
cd waterberry
cd public && npm install
cd ../
pipenv install
pipenv shell
