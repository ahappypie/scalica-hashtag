FROM ubuntu:16.04

MAINTAINER Brian bb1718@nyu.edu

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y \
  python \
  python-pip \
  mysql-server \
  libmysqlclient-dev \
  python-dev \
  python-virtualenv

COPY first_install.sh /init/
COPY requirements.txt /init/
COPY db /init/
COPY web /opt/

RUN cd /init/ \
  ./first_install.sh \
  cd db \
  ./install_db.sh \
  cd

RUN source ./env/bin/activate \
  cd opt/web/scalica \
  python manage.py makemigrations micro \
  python manage.py migrate \

EXPOSE 8000
CMD python opt/web/scalica/manage.py runserver
