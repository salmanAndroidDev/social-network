FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1


# Install postgres client
RUN apk add --update --no-cache postgresql-client

# Install individual dependencies
# so that we could avoid installing extra packages to the container
RUN apk add --update --no-cache --virtual .tmp-build-deps \
	gcc libc-dev linux-headers postgresql-dev zlib-dev


COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Remove dependencies
RUN apk del .tmp-build-deps

RUN mkdir /backend
WORKDIR /backend
COPY ./backend /backend