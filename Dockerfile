FROM ubuntu:18.04

MAINTAINER yuanyifan tsingjyujing@163.com

RUN apt-get update && \
    apt-get install -y python3-pip python3-dev && \
    pip3 install --upgrade pip && \
    pip3 install django pymongo && \
    mkdir /app && \
    apt autoremove && \
    apt clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY ./* /app/
EXPOSE 80
VOLUME /data

CMD ['/usr/bin/python3','/app/docker_start.py']