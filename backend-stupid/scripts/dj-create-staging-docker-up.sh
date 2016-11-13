eval $(docker-machine env staging)
docker-compose -f docker-compose-staging.yml build
docker-compose -f docker-compose-staging.yml run django python manage.py makemigrations
docker-compose -f docker-compose-staging.yml run django python manage.py migrate
docker-compose -f docker-compose-staging.yml up