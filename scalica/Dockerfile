FROM ubuntu:16.04

MAINTAINER Brian bb1718@nyu.edu

ENV DEBIAN_FRONTEND noninteractive

ARG mysql_pass

RUN apt-get update && apt-get install -y \
  python \
  python-pip \
  libmysqlclient-dev \
  python-dev \
  python-virtualenv

RUN apt-get install -y mysql-server \
  debconf-set-selections <<< "mysql-server mysql-server/root_password password $mysql_pass" \
  debconf-set-selections <<< "mysql-server mysql-server/root_password_again password $mysql_pass"

RUN mkdir scalica && mkdir scalica/db && mkdir scalica/web

COPY first_install.sh /scalica/
COPY requirements.txt /scalica/
COPY db /scalica/db/
COPY web /scalica/web/

RUN cd /scalica/ \
  ./first_install.sh \
  ./db/install_db.sh <<< $mysql_pass
  source ./env/bin/activate \
  cd web/scalica \
  python manage.py makemigrations micro \
  python manage.py migrate

EXPOSE 8000

RUN cd /scalica/ \
  source ./env/bin/activate \
  python web/scalica/manage.py runserver
