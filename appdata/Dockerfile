FROM gliderlabs/alpine:latest

RUN apk-install mysql mysql-client

COPY src /
RUN /root/install_mysql.sh

VOLUME /var/lib/mysql
CMD /bin/sh
