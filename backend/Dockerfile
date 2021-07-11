FROM python:3.7-alpine3.9

ENV OJ_ENV production

ADD . /app
WORKDIR /app

HEALTHCHECK --interval=5s --retries=3 CMD python /app/deploy/health_check.py

RUN apk add --update --no-cache build-base nginx openssl curl unzip supervisor jpeg-dev zlib-dev postgresql-dev freetype-dev && \
    pip install --no-cache-dir -r /app/deploy/requirements.txt && \
    apk del build-base --purge

RUN curl -L  https://github.com/skku-npc/skku-coding-platform/releases/download/v0.1-alpha/dist.tar.gz -o dist.tar.gz && \
    tar -zxf dist.tar.gz && \
    rm dist.tar.gz

ENTRYPOINT /app/deploy/entrypoint.sh
