#!/bin/bash

NAME=Joe
HOMEDIR=/home/danny/PycharmProjects
DJANGODIR=${HOMEDIR}/${NAME}
SOCKFILE=/tmp/${NAME}.sock
NUM_WORKERS=3
DJANGO_WSGI_MODULE=${NAME}.wsgi
GUNICORN=${HOMEDIR}/${NAME}/venv/bin/gunicorn

cd $DJANGODIR
source ${HOMEDIR}/${NAME}/venv/bin/activate

# Если по какой-то причине директории с SOCKFILE не существует -- создаем её
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR
# Запускаем наш Django-проект
# Опционально можем записывать Debug в лог файлы (или другие файлы)
exec ${GUNICORN} ${DJANGO_WSGI_MODULE}:application \
  --workers $NUM_WORKERS \
  #--bind unix:${SOCKFILE} \
# добавляем если настройки проекта хранятся в не стандартном модуле
# --env DJANGO_SETTINGS_MODULE=settings.production \
# --log-level=debug \
# --log-file=-