#!/bin/sh

if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL started"
fi


# * This should be taking care of by the developer who created the model.
# python manage.py makemigrations
python manage.py migrate
# python manage.py makemessages
# python manage.py compilemessages
# python manage.py flush --no-input
python manage.py collectstatic --noinput --clear
python manage.py runscript create_site --script-arg staging

# nohup python manage.py qcluster | tee /dev/stdout & # Start the q-cluster
# ( sleep 86400 && kill 1 && sleep 10 && kill -9 1 )&
# echo "Running Celery Worker ..."
# celery -A django_monolith_vite worker -l info --detach
# echo "Running Celery Beat ..."
# celery -A django_monolith_vite beat -l info --detach

# https://docs.docker.com/engine/reference/builder/#understand-how-cmd-and-entrypoint-interact
exec "$@"
