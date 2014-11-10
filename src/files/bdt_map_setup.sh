cd /home
mkdir /var/www/html/map

svn checkout https://v-db-svn01.office.iseoptions.com/svn/repos/ISE/ASGScripts/TestAutomation/BDT_MAP/trunk /home/SVN_BDT_MAP
svn checkout https://v-db-svn01.office.iseoptions.com/svn/repos/ISE/ASGScripts/TestAutomation/trunk/RobotFramework /home/SVN_RobotFramework

ln -s /home/SVN_BDT_MAP/map_frontend_web_gui/* /var/www/html/map*
