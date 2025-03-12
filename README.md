# open-feed-reader
An open source rss feed website for those who want to host their own.

## Docker
Build the docker container using:
```bash
docker build -t progradedv/open-feed-reader:v0.1.1 --no-cache --ssh default.
```

### Port
By default the web app will be available on port 8000. Forward this port at your own risk.

### Database
This project requires you run your own postgresql database, and link to it using environement variables.

An example docker-compose.yml is provided.

### Media
User uploaded media will be stored internally at "/media", extend a volume to this folder to store the files externally, preserving them through updates.

### Required Environment Variables
The app will likely crash on launch if these are not present.
| Key | Description |
| ----------- | ----------- |
| SECRET_KEY | a salted key |
| POSTGRES_HOST | The url to reach the postgresql database |
| POSTGRES_DB | The database name |
| POSTGRES_USER | The database username |
| POSTGRES_PASSWORD | The database password |
| CSRF_TRUSTED_ORIGINS | A list of trusted origins for unsafe requests (e.g. POST) | 

### Optional Environment Variables
These variables are not required to run the app but are probably needed for production.
| key | Default | Description
| ----------- | ----------- | ----------- |
| DEBUG | False | Set to true to activate debug mode. Do NOT run True in production. |
| ALLOWED_HOSTS | "[]" | A list of strings representing the host/domain names that this Django site can serve |
| EMAIL_HOST_USER | | The email address to send password resets and other notifications from
| EMAIL_HOST_PASSWORD | | A password to the website email address. Do not use your real password, use an app-password or other secondary permissions

#### command to import a .env file
```bash
export $(grep -v '^#' .env | xargs -d '\n')
```
Or you can add this to .bash_aleases:
```bash
senv() { set -a && source .env && set +a; }
```
This adds the terminal command 'senv' witch will import environment variables from a .env file.

### HTTPS
This container is not meant to handle https connections. It expects them to be handled via nginx, apache, or other network manager

## Administration

### Create Super User
Run this command from within the container to create a superuser.
`python manage.py createsuperuser`

### Updating Feeds
Run this command within the container to update all feeds.
`python manage.py refreshfeeds`
It is recommended using cron to run it every 5-20 minutes

### Permissions
- Any user with the feeds.add_source, feeds.change_source, feeds.delete_source permissions can add, edit, and delete sources
