FROM alpine:3.2

RUN apk add --update \
      mariadb \
      mariadb-client \
    && rm -f /var/cache/apk/*

COPY src /
RUN /root/install_mysql.sh

VOLUME /var/lib/mysql
CMD /bin/sh
