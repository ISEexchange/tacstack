FROM gliderlabs/alpine:3.1

RUN apk-install mysql mysql-client

COPY src /
RUN /root/install_mysql.sh

VOLUME /var/lib/mysql
CMD /bin/sh
