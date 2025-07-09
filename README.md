# open-feed-reader
An open source rss feed website for those who want to host their own.


# Install
Install the dependancies: `pip isntall -r requirements.txt`

# Environment Variables
The app will not launch if these environment variables are not present
| Required Key | Description |
| ----------- | ----------- |
| SECRET_KEY | a salted key |

These variables are not required to run the app but are essential for production security or debugging.
| Optional key | Default | Description
| ----------- | ----------- | ----------- |
| DEBUG | False | Set to true to activate the django debug mode. Do NOT run True in production. |
| ENABLE_SIGNUPS | False | if this value is false than new users will not be able to create new accounts.
| ALLOWED_HOSTS | "[]" | A list of strings representing the host/domain names that this Django site can serve |
| CSRF_TRUSTED_ORIGINS | "[]" | A list of trusted origins for unsafe requests (e.g. POST) |
| EMAIL_HOST_USER | | The email address to send password resets and other notifications from
| EMAIL_HOST_PASSWORD | | A password to the website email address. Do not use your real password, use an app-password or other secondary permissions
| CASH_ENABLED | True | Set this to false to disable the built in page caching.
| REDIS_LOCATION | | If provided then OFR will use a redis instance at this location as the cache. If not provided then OFR will use a local memory cache.

**Postgress** is my database of choice for production environments, but if you don't provide this information then OFR will use sqlite

| Postgress Key | Description |
| ----- | ----- |
| POSTGRES_HOST | The url to reach the postgresql database |
| POSTGRES_DB | The database name |
| POSTGRES_USER | The database username |
| POSTGRES_PASSWORD | The database password |

## .env file
When running OFR from a terminal it is usefull to set all the nesisary environment variables in a `.env` file. e.g.:
```
SECRET_KEY=1234567890qwertyuiop

SQLITE_DB=db.sqlite3

ALLOWED_HOSTS=localhost
CSRF_TRUSTED_ORIGINS=http://localhost:8000
DEBUG=True
```

This is the linux command to import it:
```bash
export $(grep -v '^#' .env | xargs -d '\n')
```
Or you can add this function to ~/.bash_aleases:
```bash
senv() { set -a && source .env && set +a; }
```
This adds the terminal command 'senv' witch will import environment variables from an .env file in your current directory.

# Run
For delevopment, It is recomended to use the default django server:
```bash
python app/manage.py runserver 0.0.0.0:8000
```
For production, it is recomended to use gunicorn:
```bash
gunicorn open_feed_reader.wsgi:application --bind 0.0.0.0:8000
```


## Docker
OFR comes with a Dockerfile. Build the docker container using:
```bash
docker build -t progradedv/open-feed-reader:dev --ssh default=~/.ssh/id_rsa .
```

## Docker Compose
OFR comes with a few docker compose files.
- **docker-compose.dev.yaml** is a simple development set up that only used the OFR container with a sqllte database.
- **docker-compose.prod.yaml** is an example productions environment that uses a redis instance for caching, a nginx instance for static files, and a postgres database.

### HTTPS
This application is not meant to handle https connections. It expects them to be handled via nginx, apache, or other network manager

## Administration

### Create Super User
Run this command from within the container to create a superuser.
`python manage.py createsuperuser`

### Updating Feeds
Run this command within the container to update all feeds.
`python manage.py refreshfeeds`
It is recommended using cron to run it every 5-20 minutes

### Permissions
- Any user with the feeds.add_source, feeds.change_source, or feeds.delete_source permissions can add, edit, and delete sources.
