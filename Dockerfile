FROM python:3.11

# clean up the python logging
ENV PYTHONBUFFERED=1
ENV PIP_ROOT_USER_ACTION=ignore

# nesisary for importing packags from github
RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

WORKDIR /app

# import requirements
COPY ./requirements.txt .
RUN --mount=type=ssh pip install -r requirements.txt

# add app
COPY ./app .

CMD python manage.py runserver 0.0.0.0:8000
