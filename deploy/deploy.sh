#!/bin/bash

export APP_NAME=cafe-search
export TEST_RANGE=30

NCP_HOST=$NCP_DOCKER_HOST:$NCP_DOCKER_PORT
BASE_DIR=$PWD
CA_PATH="$BASE_DIR/ca.pem"
CERT_PATH="$BASE_DIR/cert.pem"
KEY_PATH="$BASE_DIR/key.pem"

EXIST_BLUE=$(docker-compose -H $NCP_HOST --tlscacert=$CA_PATH --tlscert=$CERT_PATH --tlskey=$KEY_PATH --tlsverify -p $APP_NAME-blue -f docker-compose-blue.yml ps | grep Up)

if [ -z "${EXIST_BLUE}" ]; then
    echo "blue up"
    IDLE_PORT=8000
    docker-compose -H $NCP_HOST --tlscacert=$CA_PATH --tlscert=$CERT_PATH --tlskey=$KEY_PATH --tlsverify -p $APP_NAME-blue -f docker-compose-blue.yml up -d

else
    echo "green up"
    IDLE_PORT=8001
    docker-compose -H ${NCP_HOST} --tlscacert=$CA_PATH --tlscert=$CERT_PATH --tlskey=$KEY_PATH --tlsverify -p $APP_NAME-green -f docker-compose-green.yml up -d
fi 

echo "Health check 시작합니다."
echo "curl -s http://0.0.0.0:$IDLE_PORT/health"
sleep 1

for retry_count in {1..$TEST_RANGE}
do

response=$(curl -s http://0.0.0.0:$IDLE_PORT/health)
up_count=$(echo $response | grep 'UP' | wc -l)

if [ $up_count -ge 1 ]
then
    echo "Health check 성공"
    break
else    
    echo "Health check: ${response}"
fi

if [ $retry_count -eq $TEST_RANGE ]
then
    echo "Health Check 실패. "
    echo "배포를 종료합니다."
    exit 1
fi
done

docker -H $NCP_HOST --tlscacert=$CA_PATH --tlscert=$CERT_PATH --tlskey=$KEY_PATH --tlsverify exec proxy sh /scripts/switch-serve.sh $IDLE_PORT
docker -H $NCP_HOST --tlscacert=$CA_PATH --tlscert=$CERT_PATH --tlskey=$KEY_PATH --tlsverify exec proxy service nginx reload

if [ -z "${EXIST_BLUE}" ]; then
    docker-compose -H $NCP_HOST --tlscacert=$CA_PATH --tlscert=$CERT_PATH --tlskey=$KEY_PATH --tlsverify -p $APP_NAME-green -f docker-compose-green.yml down

else
    docker-compose -H $NCP_HOST --tlscacert=$CA_PATH --tlscert=$CERT_PATH --tlskey=$KEY_PATH --tlsverify -p $APP_NAME-blue -f docker-compose-blue.yml down
fi
echo "배포 성공 Proxy Port: $IDLE_PORT"
exit 0  
