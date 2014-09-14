# Centos 6.5
FROM jumanjiman/puppetagent

ADD src /tmp/src
RUN echo "NETWORKING=yes" > /etc/sysconfig/network
RUN puppet apply --modulepath=/tmp /tmp/src/test/init.pp

RUN /files/oval-vulnerability-scan.sh

EXPOSE 22 80 3606

ADD supervisord.conf /etc/

CMD ["supervisord", "-n"]
