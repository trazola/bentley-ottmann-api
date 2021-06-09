# pull official slim python image
FROM python:3.9.5-slim

# set python env vars
ENV PYTHONDONTWRITEBYTECODE 1 \
    && PYTHONUNBUFFERED 1

# install OS dependencies
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install poetry

# create current workdir
WORKDIR app

# copy all project
COPY . .

# install python package
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

RUN ["chmod", "+x", "docker-entrypoint.sh"]

ENTRYPOINT ["sh", "./docker-entrypoint.sh"]