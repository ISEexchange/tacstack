Further Instructions
-------------

Now that you have your container you need to set it up so its functional.

Import FTP Data
-------------

If there is an existing FTP data volume export its contents using the command below. Change the `--volumes-from` argument and the name of the resulting tar file:

    docker run --rm --volumes-from ftpdatavolprod_old -v $(pwd):/backup gliderlabs/alpine:latest tar cvf /backup/ftpdata_2015_03_29.tar /var/ftp/pub/uploads/

Now import the tar ball into your just-created container using the command below. Change the `--volumes-from` argument and the name of the tar file:

    docker run --rm -it --volumes-from ftpdatavolprod_new -v $(pwd):/backup gliderlabs/alpine:latest tar xvf /backup/ftpdata_2015_03_29.tar

Import MySQL Data
-------------

To import an existing map_db, you should have a backup .sql file available. If you first need to get the .sql file onto the CoreOS host, one way to do it is:

    [user@tc-oat01 tmp]$ scp -i ~/.ssh/id_rsa map_db_dump_2015-04-16.sql core@td-tac01:/home/core
    map_db_dump_2015-04-16.sql                                      100%  776KB 776.5KB/s   00:00

Now get the .sql file from the CoreOS host into your container:

    # Get your docker containers IP address
    docker inspect tacstack_mapappprod_1 | grep IPAddress

    # scp the file into the container
    scp map_db_dump_2015-04-16.sql root@<IPAddress>:/home

Then enter the container:

    docker exec -it tacstack_mapappprod_1 /bin/bash

Now, import the .sql file:

    cd /home
    mysql < map_db_dump_2015-04-16.sql

There is a script for setting up the necessary directories:

    chmod +x bdt_map_setup.sh
    ./bdt_map_setup.sh

This has created the web directories, downloaded the bdt and robotframework repos,
changed the DocumentRoot for the httpd service and a few other things.

At this point, the MAP front end website it up and running which you can visit using your browser:

    http://<your-domain>/

Lets start up the Python backend now:

    supervisorctl start map

MAP can now handle test requests, but it cannot handle deployments. For this you need to add SVC_UC4s
keys. Get the keys and update the following two files in your container:

    /home/SVC_UC4/.ssh/id_rsa
    /home/SVC_UC4/.ssh/id_rsa.pub

Now MAP can handle deployments too.

The container is now complete. Enjoy!
