FROM python:3.13

# clean up the python logging
ENV PYTHONBUFFERED=1
ENV PIP_ROOT_USER_ACTION=ignore

# nesisary for importing packags from github
RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

WORKDIR /app

# import requirements
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN --mount=type=ssh pip install git+ssh://git@github.com/ProgradeDV/django-user-management.git@v0.2.0
RUN --mount=type=ssh pip install git+ssh://git@github.com/ProgradeDV/django-feed-reader.git@v0.2.0

# add app
COPY ./app .

RUN python manage.py collectstatic
CMD python manage.py runserver 0.0.0.0:8000
