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

# Clone the bdt repo
cd /home
git clone https://github.com/ISEexchange/bdt.git

# Switch to the develop branch
if [ ! -z "$1" ] ; then
    if [ "$1" == "develop" ] ; then
        echo "Checking out develop branch"
        cd bdt
        git checkout -b develop
        git fetch origin
        git rebase origin/develop
    fi
fi

# Clone the robot framework repo
cd /home
git clone https://github.com/ISEexchange/robotframework.git

# Clone the docker-t7 repo
cd /home
git clone https://github.com/ISEexchange/docker-t7.git

# Create symlinks
cd /home/bdt/map/src/map_frontend_web_gui
find -maxdepth 1 | awk '{print substr($1, 3)}' | while read file; do ln -s "$PWD/$file" "/var/www/localhost/htdocs/map/$file" ; done

cd /home
ln -s /var/ftp/pub/uploads /var/www/localhost/htdocs/map/results
ln -s /var/ftp/pub/uploads/reports/ /var/www/localhost/htdocs/map/reports

chmod 644 /etc/phpmyadmin/config.inc.php
chmod 600 /root/.ssh/config

sed -i 's,DocumentRoot "/var/www/localhost/htdocs",DocumentRoot "/var/www/localhost/htdocs/map",g' /etc/apache2/httpd.conf
supervisorctl restart httpd

source ~/.proxy
cd /home/bdt/map/src/map_nodejs_server
npm install

supervisorctl start map
supervisorctl start nodejs
