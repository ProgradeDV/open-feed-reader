# Deployment Notes

## Build the docker container
deploy the 
```shell
docker build -t open-feed-reader:0.6.1.dev .
```

## Pack up the docker container
```shell
docker save open-feed-reader:0.6.1.dev > open-feed-reader.tar
```

## Import the packed container
```shell
docker load --input open-feed-reader.tar
```

## Initial database setup
Run these commands from within the web container in order to set up the database and populate it.
```shell
python app/manage.py migrate
python app/manage.py createsuperuser
```

## Apply Updates
Run these commands from within the web container in order to apply any changes to the persistant volumes.
```shell
python app/manage.py migrate
python app/manage.py collectstatic
```
_You will probably need to purge the nginx/cloudflare cache and restart_

# Docker Compose

## Start a compose app
```shell
docker compose up -d
```

## run a command from inside a compose app
```shell
docker compose exec web ...
```
