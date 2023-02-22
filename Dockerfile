# syntax=docker/dockerfile:1
FROM node:16.17-slim as builder

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends \
    g++ \
    build-essential \
    python3 \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /prj

RUN npm install -g pnpm
COPY ./package.json ./pnpm-lock.yaml /prj/
RUN set -ex && pnpm install --frozen-lockfile
COPY ./tsconfig.json ./vite.config.ts /prj/

COPY ./frontend/ /prj/frontend/
RUN pnpm build


FROM python:3.10-slim

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends \
    g++ \
    build-essential \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /prj

COPY ./Pipfile ./Pipfile.lock /prj/

RUN pip install --upgrade pip && pip install pipenv
RUN set -ex && pipenv install --deploy --system --clear

COPY ./app/ /prj/app/
COPY --from=builder /prj/frontend/dist/ /prj/frontend/dist/

WORKDIR /prj/app
RUN python3 ./manage.py collectstatic --noinput

CMD [ "uwsgi", "uwsgi.ini" ]
