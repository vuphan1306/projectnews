eval $(docker-machine env pdev)
echo "START BUILD DOCKER IMAGE"
docker-compose -f dev.yml build
echo "START Makemigrations!"
docker-compose -f dev.yml run django python manage.py makemigrations
echo "START Migrate!"
docker-compose -f dev.yml run django python manage.py migrate
echo "START Run Up!"
docker-compose -f dev.yml up