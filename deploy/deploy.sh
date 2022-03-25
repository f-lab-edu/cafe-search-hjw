#!/bin/bash

APP_NAME=cafe-search
DEPLOY_DIR=/root/jw/git-action/deploy

EXIST_BLUE=$(docker-compose -p ${APP_NAME}-blue -f ${DEPLOY_DIR}/docker-compose-blue.yml ps | grep Up)

if [ -z "$EXIST_BLUE" ]; then
    echo "blue up"
    IDLE_PORT=8000
    docker-compose -p ${APP_NAME}-blue -f ${DEPLOY_DIR}/docker-compose-blue.yml up -d

else
    echo "green up"
    IDLE_PORT=8001
    docker-compose -p ${APP_NAME}-green -f ${DEPLOY_DIR}/docker-compose-green.yml up -d
fi 

echo "> Health check 시작합니다."
echo "> curl -s http://0.0.0.0:$IDLE_PORT/health"
sleep 1

for retry_count in {1..100}
do
response=$(curl -s http://0.0.0.0:$IDLE_PORT/health)
up_count=$(echo $response | grep 'UP' | wc -l)

if [ $up_count -ge 1 ]
then
    echo "> Health check 성공"
    break
else
    echo "> Health check: ${response}"
fi

if [ $retry_count -eq 100 ]
then
    echo "> Health check 실패. "
    echo "> Nginx에 연결하지 않고 배포를 종료합니다."
    exit 1
fi
done

docker exec -it proxy sh /scripts/switch-serve.sh ${IDLE_PORT}
docker exec -it proxy service nginx reload

if [ -z "$EXIST_BLUE" ]; then
    docker-compose -p ${APP_NAME}-green -f ${DEPLOY_DIR}/docker-compose-green.yml down

else
    docker-compose -p ${APP_NAME}-blue -f ${DEPLOY_DIR}/docker-compose-blue.yml down
fi
echo "> 배포 성공 Nginx Current Proxy Port: $IDLE_PORT"
exit 0