FROM python:3.10.14-slim-bookworm

# Python não faz buffer de string, o que faz com seja mais rápido a saida dos comandos
ENV PYTHONUNBUFFERED 1

ENV PYTHONDONTWRITEBYTECODE 1

# Copiando os requirments
COPY ./dev.requirements.txt /tmp/dev.requirements.txt
COPY ./production.requirements.txt /tmp/production.requirements.txt
COPY ./app /app/

WORKDIR /app


EXPOSE 8000

ARG DEV=false

RUN apt-get update && \
  apt-get -y install libpq-dev gcc && \
  python -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install -r /tmp/production.requirements.txt && \
  if [ $DEV="true" ]; \
  then /venv/bin/pip install -r /tmp/dev.requirements.txt; \
  fi && \
  rm -rf /tmp && \
  adduser --disabled-password --no-create-home django-user

ENV PATH="/venv/bin:$PATH"

USER django-user






