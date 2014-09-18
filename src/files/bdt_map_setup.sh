cd /home
svn checkout https://v-db-svn01.office.iseoptions.com/svn/repos/ISE/ASGScripts/TestAutomation/trunk/BDT_MAP SVN_BDT_MAP

mkdir /var/www/html/map
ln -s /home/SVN_BDT_MAP/trunk/map_frontend_web_gui/* /var/www/html/map*
