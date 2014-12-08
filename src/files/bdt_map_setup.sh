# Make directories needed for viewing site
mkdir /var/www/html/map
mkdir /var/www/html/map/results

# Perform SVN Checkouts
svn checkout https://v-db-svn01.office.iseoptions.com/svn/repos/ISE/ASGScripts/TestAutomation/BDT_MAP              /home/SVN_BDT_MAP
svn checkout https://v-db-svn01.office.iseoptions.com/svn/repos/ISE/ASGScripts/TestAutomation/trunk/RobotFramework /home/SVN_RobotFramework

#Link checkouts with site path
ln -s /home/SVN_BDT_MAP/trunk/map_frontend_web_gui/* /var/www/html/map*
ln -s /var/ftp/pub/uploads /var/www/html/map/results

# Steps for deployment
mkdir /home/SVC_UC4
mkdir /home/SVC_UC4/.ssh
touch /home/SVC_UC4/.ssh/id_rsa
touch /home/SVC_UC4/.ssh/id_rsa.pub
chmod 600 /home/SVC_UC4/.ssh/id_rsa
chmod 644 /home/SVC_UC4/.ssh/id_rsa.pub
