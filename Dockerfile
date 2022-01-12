# Build Stage
FROM node:14-alpine AS builder

ADD ./frontend /build
WORKDIR /build

RUN yarn install && \
    yarn build

# Deploy Stage
FROM python:3.8.12-alpine3.15

ENV OJ_ENV production
ENV NODE_ENV production

ADD ./backend /app
WORKDIR /app

HEALTHCHECK --interval=5s --retries=3 CMD python /app/deploy/health_check.py

RUN apk add --update --no-cache build-base nginx openssl curl unzip supervisor jpeg-dev zlib-dev postgresql-dev freetype-dev && \
    pip install --no-cache-dir -r /app/deploy/requirements.txt && \
    apk del build-base --purge

COPY --from=builder /build/dist /app/dist

ENTRYPOINT /app/deploy/entrypoint.sh
