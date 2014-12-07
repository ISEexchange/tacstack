# Make directories needed for viewing site
mkdir /var/www/html/map
mkdir /var/www/html/map/results

# Perform SVN Checkouts
svn checkout https://v-db-svn01.office.iseoptions.com/svn/repos/ISE/ASGScripts/TestAutomation/BDT_MAP              /home/SVN_BDT_MAP
svn checkout https://v-db-svn01.office.iseoptions.com/svn/repos/ISE/ASGScripts/TestAutomation/trunk/RobotFramework /home/SVN_RobotFramework

#Link checkouts with site path
ln -s /home/SVN_BDT_MAP/map_frontend_web_gui/* /var/www/html/map*
ln -s /var/ftp/pub/uploads /var/www/html/map/results

# Steps for deployment
mkdir /home/SVC_UC4
mkdir /home/SVC_UC4/.ssh
mv    /home/config /home/SVC_UC4/.ssh/
