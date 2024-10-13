#!/bin/bash

alembic upgrade head

cd conf_shed

gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000