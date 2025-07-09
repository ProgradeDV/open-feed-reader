###########
# BUILDER #
###########

# pull official base image
FROM python:3.13-alpine AS builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install system dependencies
RUN apk update && apk upgrade
RUN pip install --upgrade pip

# install python dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

#########
# FINAL #
#########

# pull official base image
FROM python:3.13-alpine

# create the app user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# create the appropriate directories
ENV HOME=/home/app
RUN mkdir -p $HOME
RUN mkdir /home/sqlite/
WORKDIR $HOME

# install dependencies
RUN apk update && apk upgrade
COPY --from=builder /usr/src/app/wheels /wheels

RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy project
COPY ./nginx /home/nginx
COPY ./app .

# make entrypoint.prod.sh runable
RUN sed -i 's/\r$//g'  $HOME/entrypoint.prod.sh
RUN chmod +x $HOME/entrypoint.prod.sh

# chown all the files to the app user
RUN chown -R appuser:appgroup $HOME
RUN chown -R appuser:appgroup /home/sqlite/

# change to the app user
USER appuser

# run entrypoint.prod.sh
ENTRYPOINT ["/home/app/entrypoint.prod.sh"]
CMD ["gunicorn", "open_feed_reader.wsgi:application", "--bind", "0.0.0.0:8000"]
