# open-feed-reader
An open source rss feed website for those who want to host their own.

This app is a Djengo project witch can either be run raw from a python environment or as a docker container.

![Alt text](/screenshots/screenshot_home.png?raw=true "Optional Title")

# Environment Variables
| Required Variable | Description |
| ----------- | ----------- |
| SECRET_KEY | a salted key |

debuging, or enabling features.
| Optional Variable | Default | Description
| ----------- | ----------- | ----------- |
| DEBUG | False | Set to true to activate the django debug mode. Do NOT run True in production. |
| ENABLE_SIGNUPS | False | if this value is false than new users will not be able to create new accounts.
| ALLOWED_HOSTS | "[]" | A list of strings representing the host/domain names that this Django site can serve |
| CSRF_TRUSTED_ORIGINS | "[]" | A list of trusted origins for unsafe requests (e.g. POST) |
| EMAIL_HOST_USER | | The email address to send password resets and other notifications from
| EMAIL_HOST_PASSWORD | | A password to the website email address. Do not use your real password, use an app-password or other secondary permissions
| CASHE_ENABLED | True | Set this to false to disable the built in page caching.
| REDIS_LOCATION | | If provided then OFR will use a redis instance at this location as the cache. If not provided then OFR will use a local memory cache.

**Postgress** is my database of choice for production environments, but if you don't provide this information then OFR will use sqlite.

| Postgress Key | Description |
| ----- | ----- |
| POSTGRES_HOST | The url to reach the postgresql database |
| POSTGRES_DB | The database name |
| POSTGRES_USER | The database username |
| POSTGRES_PASSWORD | The database password |

## .env file
When running OFR it is usefull to set all the nesisary environment variables in a `.env` file.

There are two examples of .env files included in this project, `example.dev.env` and `example.prod.env`.

If you want to set thes variables in your terminal session, this is the linux command to import a .env file:
```bash
export $(grep -v '^#' .env | xargs -d '\n')
```
Or you can add this function to ~/.bashrc. This defines a terminal command 'senv'.
```bash
senv() { set -a && source .env && set +a; }
```

# Run locally in terminal
To run OFR locally in the terminal, I recoment using a python venv.
```bash
# create the venv
python -m venv .venv
# activate the venv
./.venv/bin/activate
```
Install the dependancies:
```bash
pip install -r requirements.txt
```

For delevopment, It is recomended to use the default django server:
```bash
python app/manage.py runserver 0.0.0.0:8000
```
For production, it is recomended to use gunicorn. This command is what the docker container will run by default.
```bash
gunicorn open_feed_reader.wsgi:application --bind 0.0.0.0:8000
```

## Deployment with Docker Compose
OFR comes with a few docker compose files.
- **docker-compose.yaml** is the sinple set up. It will use an internal sqlite database, and local memory caching.
- **docker-compose.prod.yaml** is an example production environment that uses a redis instance for caching, an nginx instance for static files, and a postgres database.

### HTTPS
This application is not meant to handle https connections, only http. It expects this to be handled via nginx, apache, or other network manager.

## Administration

### Create Super User
Run this command to create a superuser, the app will probably fail to run if no superuser exists.
```bash
python manage.py createsuperuser
```

### Set up the database
```bash
python manage.py migrate
```

### Updating Feeds
Run this command to update feeds.
```bash
python manage.py refreshfeeds {--max n} {--all-feeds} {--no-cache}
```
It is recommended to use cron to run it every 5-20 minutes.
 - if **--max** is set then only the n oldest feeds will be refreshed
 - if **--all-feeds** is NOT set then OFR will skip feeds that have have recent content. The amount of time OFR will wait depends on the frequency of content
 - if **--no-cache** is present then OFR will refrech feeds without the header data that some servers will use to only send back new content.
