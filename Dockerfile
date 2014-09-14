# Centos 6.5
FROM jumanjiman/puppetagent

# Commenting out the following until its needed
# ADD src /tmp/src
# RUN echo "NETWORKING=yes" > /etc/sysconfig/network
# RUN puppet apply --modulepath=/tmp /tmp/src/test/init.pp
# Removing for now until script is added
# RUN /files/oval-vulnerability-scan.sh


# install packages
RUN yum -y install \
    httpd vim-enhanced bash-completion unzip \
    mysql mysql-server \
    php php-mysql php-devel php-gd php-pecl-memcache php-pspell php-snmp php-xmlrpc php-xml \
    openssh-server openssh-clients passwd \
    python python-pip python-nose python-pep8 \
    gcc \
    mysql-devel python-devel \
    ; yum clean all
    
RUN yum -y groupinstall 'Development tools'
RUN echo "NETWORKING=yes" > /etc/sysconfig/network
RUN service mysqld start

RUN yum -y install \
    libxslt-devel libxslt libxslt-python \
    libxml2-devel libxml2 libxml2-python \
    python-lxml \
    ; yum clean all

# install supervisord
RUN pip install "pip>=1.4,<1.5" --upgrade
RUN pip install supervisor MySQL-python robotframework lxml

EXPOSE 22 80 3606

ADD /src/files/supervisord.conf /etc/

CMD ["supervisord", "-n"]
