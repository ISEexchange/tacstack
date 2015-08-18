
# Set date time variable
dt=`date +"%Y%m%d-%H%M%S"`

cd ..

# First backup the FTP directory
docker run --rm --volumes-from tacstack_ftpdatavolprod_1 -v $(pwd):/backup alpine:latest tar cvf /backup/ftpdata_$dt.tar /var/ftp/pub/uploads/
read -p "Hit Enter to continue"

# Dump the MySQL map_db database
docker run --rm --volumes-from tacstack_mysqldatavolprod_1 quay.io/iseexchange/tacstack:latest mysqldump --socket=/var/lib/mysql/mysql.sock --routines --events --triggers --skip-extended-insert --complete-insert --flush-logs --add-drop-database --database map_db > map_db_dump_$dt.sql
read -p "Hit Enter to continue"

# In case there are local modifications, backup the git repos
docker cp tacstack_mapappprod_1:/home/bdt             bdt_repo_backup_$dt
read -p "Hit Enter to continue"
docker cp tacstack_mapappprod_1:/home/robotframework  rf_repo_backup_$dt
read -p "Hit Enter to continue"

# Now its safe to remove the running container
cd tacstack
./docker-compose -f docker-compose-prod.yml kill
read -p "Hit Enter to continue"
./docker-compose -f docker-compose-prod.yml rm -f
read -p "Hit Enter to continue"

# Download latest images
cat docker-compose-common.yml | grep image | awk '{print $2}' | while read image; do docker pull $image; done
read -p "Hit Enter to continue"

# Start up the containers
./docker-compose -f docker-compose-prod.yml up -d
read -p "Hit Enter to continue"

# Import the backed up FTP data
cd ..
docker run --rm -it --volumes-from tacstack_ftpdatavolprod_1 -v $(pwd):/backup alpine:latest tar xvf /backup/ftpdata_$dt.tar
read -p "Hit Enter to continue"

# Import the MySQL map_db database
MAPAPPIP=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' tacstack_mapappprod_1)
read -p "Hit Enter to continue"
scp map_db_dump_$dt.sql root@$MAPAPPIP:/home
read -p "Hit Enter to continue"

echo "Now enter the container with:"
echo "    docker exec -it tacstack_mapappprod_1 bash"
echo "and run the following:"
echo "    mysql < map_db_dump_$dt.sql"
echo "    chmod +x bdt_map_setup.sh"
echo "    ./bdt_map_setup.sh"
echo "Then be sure to copy in the keys for SSHing for deployments"

