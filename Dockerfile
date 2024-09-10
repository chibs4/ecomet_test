FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/

EXPOSE $PORT

RUN apt-get -yqq update && apt-get -yqq install \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev \
    ca-certificates \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY src /app

