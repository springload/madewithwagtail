FROM nginx:stable-alpine as base

RUN apk update && apk add --no-cache ca-certificates

ADD nginx.conf /etc/nginx/nginx.conf
ADD vhost.conf /etc/nginx/conf.d/default.conf
