# Frontend assets
FROM node:erbium-alpine as frontend

ENV APPLICATION madewithwagtail

COPY package.json yarn.lock /madewithwagtail/

WORKDIR /madewithwagtail

RUN apk update && apk add --virtual make \
    gcc \
    g++ \
    musl-dev \
    python3 \
    && yarn install --frozen-lockfile --production=true \
    && apk del gcc g++ musl-dev python3

COPY . /madewithwagtail/
RUN yarn dist

CMD ["yarn", "start", "--prefix", "/madewithwagtail"]

# Base backend
FROM python:3.6-alpine as base
ARG REQUIREMENTS=production.txt

ENV PYCURL_SSL_LIBRARY openssl

RUN apk update && apk add postgresql-libs libevent libjpeg openjpeg tiff zlib freetype tk libcurl su-exec git

WORKDIR /madewithwagtail

COPY requirements /madewithwagtail/requirements
COPY docker/requirements.txt /madewithwagtail/docker/requirements.txt

RUN apk update && apk add --virtual build-deps make gcc g++ musl-dev && \
  apk add --virtual build-headers postgresql-dev \
  jpeg-dev \
  zlib-dev \
  freetype-dev \
  lcms2-dev \
  openjpeg-dev \
  tiff-dev \
  tk-dev \
  tcl-dev \
  harfbuzz-dev \
  fribidi-dev \
  libevent-dev \
  curl-dev && \
  cd /madewithwagtail && \
    pip3 install -r docker/requirements.txt && \
    pip3 install -r requirements/${REQUIREMENTS} && \
    apk del build-deps build-headers

COPY --from=frontend /madewithwagtail/ /madewithwagtail/

RUN adduser -S www -u 1000 && chown -R www /madewithwagtail

ARG VERSION=dev
ENV APPLICATION_VERSION=${VERSION}
ENV DJANGO_SETTINGS_MODULE madewithwagtail.settings.hosting
ENV VERSION=${VERSION}
ENV ENVIRONMENT unknown
ENV PROJECT madewithwagtail

# base app stage
FROM base as base-app

# production stage
FROM base-app as app
ADD https://github.com/springload/ssm-parent/releases/download/v1.1.2/ssm-parent_1.1.2_linux_amd64.tar.gz /tmp/ssm-parent.tar.gz
RUN tar xvf /tmp/ssm-parent.tar.gz && mv ssm-parent /sbin/ssm-parent && rm /tmp/ssm-parent.tar.gz

ENV DJANGO_SERVER_ENV=Production
ENTRYPOINT ["/sbin/ssm-parent", "run", "-e", "-p", "/$PROJECT/common/", "-p", "/$PROJECT/$ENVIRONMENT/", "-r",  "--", "su-exec", "www"]
CMD ["/usr/local/bin/gunicorn", "--config", "/madewithwagtail/docker/gunicorn.py", "madewithwagtail.wsgi" ]

# development stage
FROM base-app as app-dev
ARG REQUIREMENTS=dev.txt
ENV DJANGO_SETTINGS_MODULE madewithwagtail.settings.dev

ADD https://raw.githubusercontent.com/mrako/wait-for/d9699cb9fe8a4622f05c4ee32adf2fd93239d005/wait-for /usr/local/bin/
RUN chmod +rx /usr/local/bin/wait-for

RUN apk add --virtual build-deps make g++ musl-dev && \
    cd /madewithwagtail && \
    pip3 install -r requirements/${REQUIREMENTS} && \
    apk del build-deps

ENTRYPOINT ["/usr/local/bin/wait-for", "database:5432", "--"]
CMD ["/usr/local/bin/gunicorn", "--config", "/madewithwagtail/docker/gunicorn.py", "--reload", "madewithwagtail.wsgi" ]

FROM app-dev as app-test
ARG REQUIREMENTS=test.txt
ENV DJANGO_SETTINGS_MODULE madewithwagtail.settings.test
RUN cd /madewithwagtail &&\
    pip install -r requirements/${REQUIREMENTS}
CMD ["/bin/sh", "/madewithwagtail/test.sh"]
