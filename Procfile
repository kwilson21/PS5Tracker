web: uvicorn --host 0.0.0.0 --port $PORT run:app --reload
worker: python -u run-worker-default.py
subscriber: python -u run-redis-subscriber.py
scheduler: rqscheduler
