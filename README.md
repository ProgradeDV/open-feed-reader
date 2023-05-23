# open-feed-reader
An open source rss feed website for those who want to host their own

# update feeds command
Run this command to update all feeds.
`python manage.py refreshfeeds`
I recomend using cron to run it every 5-20 minutes

# required environment variables
| Key | Description |
| ----------- | ----------- |
| SECRET_KEY | a salted key for secutity |
| DB_HOST | The url to reach the postgresql database |
| DB_DB | The database name |
| DB_USER | The database username |
| DB_PASSWORD | The database password |

# optional environment variables
| key | Default | Description
| ----------- | ----------- | ----------- |
| DEBUG | False | Set to true to activate debug mode |
| ALLOWED_HOSTS | "[]" | A list of strings representing the host/domain names that this Django site can serve |
