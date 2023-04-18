FROM python:3.11

ENV PYTHONBUFFERED=1
ENV PIP_ROOT_USER_ACTION=ignore

RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

WORKDIR /app
COPY ./requirements.txt .
COPY ./no_rythem_news/ .

RUN --mount=type=ssh pip install -r requirements.txt
