# open-feed-reader
An open source rss feed website for those who want to host their own.

## Setup

### Port
By default the web app will be available on port 8000. Forward this port at your own risk.

### Database
This project requires you run your own postgresql database, and link to it using environement variables.

An example docker-compose.yml is provided.

### Media
User uploaded media will be stored internally at "/media" extend a volume to this folder to store the files externally, preserving them through updates.

### Required Environment Variables
| Key | Description |
| ----------- | ----------- |
| SECRET_KEY | a salted key |
| DB_HOST | The url to reach the postgresql database |
| DB_DB | The database name |
| DB_USER | The database username |
| DB_PASSWORD | The database password |

### Optional Environment Variables
| key | Default | Description
| ----------- | ----------- | ----------- |
| DEBUG | False | Set to true to activate debug mode. Do NOT run True in production. |
| ALLOWED_HOSTS | "[]" | A list of strings representing the host/domain names that this Django site can serve |

### HTTPS
This container is not ment to handle https connections. It expects them to be handled via nginx, apache, or other network manager

## Administration

### Create Super User
Run this command from within the container to create a superuser.
`python manage.py createsuperuser`

### Updating Feeds
Run this command within the container to update all feeds.
`python manage.py refreshfeeds`
I recomend using cron to run it every 5-20 minutes

### Permissions
- Any user with the feeds.add_source, feeds.change_source, feeds.delete_source permissions can add, edit, and delete sources
