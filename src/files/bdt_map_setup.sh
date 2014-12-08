# Make directories needed for viewing site
mkdir /var/www/html/map
mkdir /var/www/html/map/results

# Perform SVN Checkouts
svn checkout https://v-db-svn01.office.iseoptions.com/svn/repos/ISE/ASGScripts/TestAutomation/BDT_MAP              /home/SVN_BDT_MAP
svn checkout https://v-db-svn01.office.iseoptions.com/svn/repos/ISE/ASGScripts/TestAutomation/trunk/RobotFramework /home/SVN_RobotFramework

#Link checkouts with site path
ln -s /home/SVN_BDT_MAP/trunk/map_frontend_web_gui/* /var/www/html/map*
ln -s /var/ftp/pub/uploads/* /var/www/html/map/results*

# Steps for deployment
mkdir /home/SVC_UC4
mkdir /home/SVC_UC4/.ssh
touch /home/SVC_UC4/.ssh/id_rsa
touch /home/SVC_UC4/.ssh/id_rsa.pub
chmod 600 /home/SVC_UC4/.ssh/id_rsa
chmod 644 /home/SVC_UC4/.ssh/id_rsa.pub

# Change the Apache web server's document root for cleaner URL
sed -i 's,DocumentRoot "/var/www/html",DocumentRoot "/var/www/html/map",g' /etc/httpd/conf/httpd.conf
sed -i 's,<Directory "/var/www/html",<Directory "/var/www/html/map",g'     /etc/httpd/conf/httpd.conf
/etc/init.d/httpd restart
