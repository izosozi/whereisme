#! /bin/bash

cd ./app

poetry run flask -A server.py --debug -e ../.env run --port 13856