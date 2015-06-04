#!/bin/sh
set -e

# This script runs during `docker build`.

# The setup step requires /run/openrc/softlevel,
# which we copy in via the Dockerfile.
/etc/init.d/mariadb setup

sock_path="/var/lib/mysql/mysql.sock"

/usr/bin/mysqld_safe --socket=$sock_path --user=mysql &
sleep 10s
echo "CREATE USER 'admin'@'localhost' IDENTIFIED BY 'changeme'; GRANT ALL PRIVILEGES ON *.* TO admin@'%' WITH GRANT OPTION; FLUSH PRIVILEGES; SET PASSWORD FOR admin@'%'=PASSWORD('changeme');" | mysql --socket=$sock_path
/usr/bin/mysqladmin --socket=$sock_path shutdown
