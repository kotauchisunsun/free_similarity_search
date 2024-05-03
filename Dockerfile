FROM debian:bookworm-slim

RUN apt-get update && apt-get install --no-install-recommends -y clang libomp-dev build-essential curl ca-certificates

ENV RYE_HOME /root/.rye
ENV PATH     ${RYE_HOME}/shims:${PATH}

RUN curl -sSf https://rye-up.com/get | RYE_INSTALL_OPTION="--yes" bash

WORKDIR /root/app

COPY . .
RUN rye sync --no-lock --no-dev
