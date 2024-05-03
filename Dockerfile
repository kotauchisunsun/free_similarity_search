FROM python:3.12.3-slim-bookworm

RUN apt-get update && apt-get install -y clang libomp-dev build-essential curl

ENV RYE_HOME /home/root/.rye
ENV PATH     ${RYE_HOME}/shims:${PATH}

RUN curl -sSf https://rye-up.com/get | RYE_INSTALL_OPTION="--yes" bash

WORKDIR /home/root/app

COPY . .
RUN rye sync
