FROM python:3.10.14-slim-bookworm

ENV PYTHONUNBUFFERED 1

ENV PYTHONDONTWRITEBYTECODE 1

# Copiando os requirments
COPY ./requirements.txt /tmp/requirements.txt

COPY ./app /app

WORKDIR /app

EXPOSE 8000

RUN python -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install -r /tmp/requirements.txt && \
  rm -rf /tmp && \
  adduser --disabled-password --no-create-home django-user

ENV PATH="/venv/bin:$PATH"

USER django-user






