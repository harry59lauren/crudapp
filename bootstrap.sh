#!/bin/sh
export FLASK_APP=./crudapp/API/api.py
pipenv shell
flask run -h 0.0.0.0