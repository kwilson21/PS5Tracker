web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT run:app
worker: python -u run-worker-default.py
subscriber: python -u run-redis-subscriber.py
scheduler: rqscheduler
