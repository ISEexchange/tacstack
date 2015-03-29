# Make directories needed for viewing site
mkdir /var/www/localhost/htdocs/map
mkdir /var/www/localhost/htdocs/map/results

# Steps for deployment
mkdir /home/SVC_UC4
mkdir /home/SVC_UC4/.ssh
touch /home/SVC_UC4/.ssh/id_rsa
touch /home/SVC_UC4/.ssh/id_rsa.pub
chmod 600 /home/SVC_UC4/.ssh/id_rsa
chmod 644 /home/SVC_UC4/.ssh/id_rsa.pub

cd /home
git clone https://github.com/ISEexchange/bdt.git

ln -s /home/bdt/map/src/map_frontend_web_gui/* /var/www/localhost/htdocs/map*
ln -s /var/ftp/pub/uploads /var/www/localhost/htdocs/map/results
ln -s /var/ftp/pub/uploads/reports/ /var/www/localhost/htdocs/map/reports

chmod 644 /etc/phpmyadmin/config.inc.php
