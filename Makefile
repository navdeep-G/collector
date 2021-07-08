.PHONY: start

export MINIO_ACCESS_KEY=ACCESS-KEY
export MINIO_SECRET_KEY=SECRET-KEY
export MINIO_URL=localhost:9000
export REDIS_PORT=6379
export REDIS_DB=0
export REDIS_URL=localhost
export ALLOW_EMPTY_PASSWORD=yes

start:
	minio server data &
	redis-server &
	python main.py