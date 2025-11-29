###########
# BUILDER #
###########

# pull official base image
FROM python:3.13-alpine AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# set work directory
WORKDIR /app

# install system dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-editable

# Copy the project into the intermediate image
ADD . .

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable

#########
# FINAL #
#########

# pull official base image
FROM python:3.13-alpine

# create the app user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

WORKDIR /app
ENV DATA_DIR=/app

# Copy the environment, but not the source code
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin
COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv

# create the media directories
RUN mkdir /app/sqlite/
RUN mkdir /app/staticfiles/
RUN mkdir /app/mediafiles/

CMD ["uv", "run", "gunicorn", "open_feed_reader.wsgi:application", "--bind", "0.0.0.0:8000"]

