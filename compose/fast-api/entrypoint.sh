#!/bin/sh
# 4 Gunicorn workers, binding Uvicorn to the main process
exec gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
