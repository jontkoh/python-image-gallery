#https://hub.docker.com/repository/docker/jontkoh/python-image-gallery
FROM ubuntu:latest
FROM postgres:11

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y && apt-get install -y build-essential python3 python3-dev python3-pip libpcre3 libpcre3-dev postgresql tzdata libpq-dev

COPY . /app/
COPY /app/createDB /app/createDB
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN useradd -m koh

EXPOSE 8888

RUN chown koh:koh app/createDB

USER koh


ENV FLASK_APP=gallery.ui.app:app
ENV FLASK_ENV=development

ENV PGDATA=/var/lib/postgresql/data/pgdata

ENV PG_HOST=image-gallery.ctzdh9pwhxzw.us-west-1.rds.amazonaws.com
ENV PG_PORT=5432
ENV IG_DATABASE=image_gallery
ENV IG_USER=image_gallery
ENV IG_PASSWD=Ontherun12!
ENV IG_PASSWD_FILE=POSTGRES_PASSWORD_FILE
ENV S3_IMAGE_BUCKET=edu.au.image-gallery

CMD ["uwsgi", "--http", ":8888", "--module", "gallery.ui.app:app", "--master", "--processes", "4", "--threads", "2"]
