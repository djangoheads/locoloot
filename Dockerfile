# syntax = docker/dockerfile:1.3
FROM python:3.11

ARG DOCKER_BUILD_REQUIREMENTS=requirements.txt

ENV DOCKER_BUILD_REQUIREMENTS=${DOCKER_BUILD_REQUIREMENTS}
ENV DJANGO_SETTINGS_MODULE=service.settings.base
ENV ROOT_PATH_FOR_DYNACONF=/home/app/config

# Install core libs
RUN apt-get --allow-releaseinfo-change update && apt-get install -y \
  postgresql-client \
  supervisor \
  apt-utils \
  python3-all-dev \
  build-essential \
  cmake \
  pkg-config \
  libx11-dev \
  libatlas-base-dev \
  libpq-dev \
  libgtk-3-dev \
  libboost-python-dev \
  software-properties-common

# Install poetry
RUN pip install poetry

RUN apt --allow-releaseinfo-change update -q \
    && apt install -y \
    libmaxminddb0 \
    libmaxminddb-dev \
    mmdb-bin

RUN apt-get install build-essential -y \
    libssl-dev \
    libffi-dev \
    python3-dev \
    cargo

RUN apt-get clean

# Install deps
COPY $DOCKER_BUILD_REQUIREMENTS /tmp/install/
WORKDIR /tmp/install
RUN pip install -r $DOCKER_BUILD_REQUIREMENTS

# Limited scope (User) context
# Prepare app user
RUN useradd --create-home app
USER app
USER root

WORKDIR /home/app

# Prepare app bin
COPY --chown=app ./entrypoint.sh /home/app/bin/entrypoint.sh
RUN chmod -R +x /home/app/bin
ENV PATH="/home/app/bin:$PATH"

# Install source code
RUN mkdir -p /home/app/libs
WORKDIR /home/app/libs
ENV PYTHONPATH="/home/app/libs"

# Move base Config
COPY --chown=app ./settings.yaml /home/app/config/

# Move app source
COPY --chown=app ./src/ /home/app/libs/

# Init static
RUN mkdir -p /var/www/static
RUN chown -R app:app /var/www/static

RUN chmod +664 -R /home/app
RUN chmod +x -R /home/app/libs

USER app

EXPOSE 8000

ENTRYPOINT ["entrypoint.sh"]

CMD ["devserver"]