FROM python:3.6.2-alpine3.6
ENV PYTHONUNBUFFERED 1

ENV DJANGO_ENV=test

# Copy Pipfile and install system-wide
# We're installing system-wide, because we currently have problems
# correctly using the entrypoint.sh, while activating the virtual environment
COPY Pipfile Pipfile.lock /tmp/
WORKDIR /tmp

# Install build dependencies for PostgreSQL. While we're at it, also install
# pipenv and all python requirements. Then remove unneeded build dependencies.
RUN apk update \
    && apk add --no-cache --virtual .build-deps \
       gcc \
       musl-dev \
    && apk add --no-cache postgresql postgresql-dev \
    && pip install pipenv \
    && pipenv install --dev --system --verbose \
    && apk del .build-deps

# Let Django collect all staticfiles
# RUN python /code/manage.py collectstatic --noinput
# RUN python /code/manage.py migrate --noinput

EXPOSE 8000

VOLUME /code
WORKDIR /code

ENTRYPOINT ["/usr/local/bin/gunicorn", "--config", "/code/gunicorn.conf", "-b", ":8000", "rodent.wsgi:application"]
