export MINIO_ACCESS_KEY='ACCESS-KEY'
export MINIO_SECRET_KEY='SECRET-KEY'
export MINIO_URL='minio1:9000'
export REDIS_URL='redis'
export REDIS_PORT=6379
export REDIS_DB=0
echo "Starting mino ..." &
minio server data &
echo "Starting Redis ..." &&
redis-server
