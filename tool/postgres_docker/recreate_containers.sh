#!/usr/bin/env bash

APP=geocode_fr
VERSION=0.1

################################################################################

ENGINE_CONTAINER=${APP}_db
DATA_CONTAINER=${ENGINE_CONTAINER}_data
DUMP_FILE_NAME=${ENGINE_CONTAINER}_dump.sql
DUMP_FILE_DIR=/backup
DUMP_FILE=${DUMP_FILE_DIR}/${DUMP_FILE_NAME}

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd ${DIR}

# backup db data
#####################################
docker start ${ENGINE_CONTAINER}
sleep 10
docker run --rm --volumes-from ${DATA_CONTAINER} -v $(pwd):${DUMP_FILE_DIR} --link ${ENGINE_CONTAINER} ${ENGINE_CONTAINER}:${VERSION} pg_dump --dbname=postgres://${APP}:${APP}@${ENGINE_CONTAINER}/${APP} -vf ${DUMP_FILE}
docker run --rm --volumes-from ${DATA_CONTAINER} -v $(pwd):${DUMP_FILE_DIR} --link ${ENGINE_CONTAINER} ${ENGINE_CONTAINER}:${VERSION} chmod ugo+w ${DUMP_FILE}
#####################################


# clean
#####################################
echo container `docker stop ${ENGINE_CONTAINER}` stopped
echo container `docker rm ${ENGINE_CONTAINER}` removed
echo container `docker rm ${DATA_CONTAINER}` removed
docker rmi ${ENGINE_CONTAINER}:${VERSION}
docker rmi ${DATA_CONTAINER}:${VERSION}
echo volume `docker volume rm ${DATA_CONTAINER}` removed
#####################################


# build/create
#####################################
docker build -f Dockerfile_data -t ${DATA_CONTAINER}:${VERSION} .
echo container `docker create --name ${DATA_CONTAINER} -v ${DATA_CONTAINER}:/var/lib/postgresql/data ${DATA_CONTAINER}:${VERSION}` created

docker build -f Dockerfile_engine -t ${ENGINE_CONTAINER}:${VERSION} .
echo container `docker create --name ${ENGINE_CONTAINER} -p 5432:5432 -v ${DATA_CONTAINER}:/var/lib/postgresql/data ${ENGINE_CONTAINER}:${VERSION}` created
#####################################


# start
#####################################
echo container `docker start ${ENGINE_CONTAINER}` started
#####################################

sleep 10

# restore db data
#####################################
docker run --rm --volumes-from ${DATA_CONTAINER} -v $(pwd)/${DUMP_FILE_NAME}:${DUMP_FILE} --link ${ENGINE_CONTAINER} ${ENGINE_CONTAINER}:${VERSION} psql --dbname=postgres://${APP}:${APP}@${ENGINE_CONTAINER}/${APP} -f ${DUMP_FILE}
#####################################

cd -
