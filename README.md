Overview
--------

This repo contains scripts and source to build multiple docker images
with Alpine Linux. The main application container has a LAMP stack of:

* Apache
* MySQL
* PHP
* Python

Build status on CircleCI (master branch): [![Circle CI](https://circleci.com/gh/ISEexchange/tacstack/tree/master.svg?style=svg&circle-token=373b7a10221a0403c993da96c45ba15ef225e932)](https://circleci.com/gh/ISEexchange/tacstack/tree/master)


How to Launch a Production System
-------------

Download this repo so you can use docker-compose files:
 
    git clone https://github.com/ISEexchange/tacstack.git
    cd tacstack

You first need to get the container images from quay.io (the 
repo in the cloud where we store our build images):

    docker-compose -f docker-compose-common.yml pull

Now start up the containers for a production system. This 
basically means that the ports will be pre-selected:

    docker-compose -f docker-compose-prod.yml up -d

Now follow the steps detailed in [MAP Setup README](MAP_Setup_README.md)

How to Launch a Test Environment
-------------

Pretty much the same as above except the docker-compose 
up command will be different:

    docker-compose -f docker-compose-testenv.yml -p mytestenv up -d

Output:

    Creating mytestenv_mysqldatavoltestenv_1...
    Creating mytestenv_ftpdatavoltestenv_1...
    Creating mytestenv_mapapptestenv_1...
    Creating mytestenv_ftpapptestenv_1...

The `-p` is what will allow you to have your own set 
of containers, independent from any other.


docker-compose Notes
-------------

docker-compose will provide a fully functioning system of containers
from scratch. It will pull all of the required images and start up
the containers. It will also take care of linking the data and app
containers and will provide ports for you to use. Use docker-compose
to create either a test environment or a production environment.

The `-d` in the `docker-compose up` command will start the 
containers/services in the background.

The ports for the test environment containers will be randomly
selected. To find them, run:

    docker-compose -f docker-compose-testenv.yml ps

Or

    docker-compose -f docker-compose-testenv.yml -p mytestenv port mapapptestenv 22

There are four services in this system that docker-compose will bring up:

    mapapp[prod|testenv]
    ftpapp[prod|testenv]
    mysqldatavol[prod|testenv]
    ftpdatavol[prod|testenv]

For more information on docker-compose:
https://docs.docker.com/compose/


Build on CircleCI
-----------------

Open a pull request on Github.
This triggers a build in CircleCI.
Dockerfiles will be built and completed docker images will be pushed to quay.io.


Pull an Already-Built Image
---------------------------

If you want the latest build of master branch:

    docker pull quay.io/iseexchange/tacstack:latest

If you want a specific version:

    # $hash refers to the git commit hash
    docker pull quay.io/iseexchange/tacstack:${hash:0:7}

If you want the version from your pull request:

    # $handle is your github handle
    # $number refers to the pull request
    docker pull quay.io/iseexchange/tacstack:${handle}_pull_${number}


Build Locally With Docker
-------------

To build the main application container, clone this git
repo, then run:

    script/build


Manual Deployment
----------

Follow these instructions if you are not using docker-compose.
For a live TAC application, run:

    docker run -d quay.io/iseexchange/tacstack_ftpdata:latest --name FTPData
    docker run -d jumanjiman/dropbox:latest
    docker run -d quay.io/iseexchange/tacstack_mysqldata:latest --name MySQLData
    docker run -d -p 18922:22 -p 80:80 -p 18906:3306 -p 18900:18900 -p 18901:18901 --name MAPApp --volumes-from MySQLData --volumes-from FTPData quay.io/iseexchange/tacstack

For an individual test environment, run:

    CID=$(docker run -d -P quay.io/iseexchange/tacstack)

    # Find the port on which sshd is running.
    docker port $CID 22

    # Find the port on which apache is running.
    docker port $CID 80


Troubleshooting
---------------

### Outside a container

```bash
# Commands for docker-compose:
# List active and exited containers.
docker-compose -f docker-compose-testenv.yml -p mytestenv ps
docker-compose ps
# Follow logs from a container.
docker-compose -f docker-compose-testenv.yml -p mytestenv logs
docker-compose logs <service-name>

# Commands for docker:
# List active containers.
docker ps
# List all containers.
docker ps -a
# Follow logs from a container.
docker logs -f <container-id>

# docker and docker-compose have similar commands. To view them:
docker-compose --help
# Or 
docker help commands
```


### Inside a container

```bash
# This example assumes the $CID variable from the "docker run" commands above.
PID=$(docker inspect --format {{.State.Pid}} $CID)
sudo nsenter --target $PID --mount --uts --ipc --net --pid

# Run various commands, then
# Press CTRL-D to exit.
```


Contributing
------------

### Continuous Integration

Each pull request triggers a build on CircleCI.
PRs cannot be merged if CI fails.


### Diff churn

Please minimize diff churn to enhance git history commands.

* Arrays should usually be multi-line with trailing commas.

* Use 2-space soft tabs and trim trailing whitespace.<br/>
  http://editorconfig.org provides editor plugins to handle this
  for you automatically based on the `.editorconfig` in this repo.


### Linear history

Use `git rebase upstream/master` to update your branch.
The primary reason for this is to maintain a clean, linear history
via "fast-forward" merges to master.
A clean, linear history in master makes it easier
to troubleshoot regressions and follow the timeline.


### Commit messages

Please provide good commit messages, such as<br/>
http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html


### Topic branch + pull request (PR)

To submit a patch, fork the repo and work within
a [topic branch](http://progit.org/book/ch3-4.html) of your fork.

1. Bootstrap your dev environment

   ```bash
   git remote add upstream https://github.com/ISEexchange/tacstack.git
   ```

1. Set up a remote tracking branch

    ```bash
    git checkout -b <branch_name>

    # Initial push with `-u` option sets remote tracking branch.
    git push -u origin <branch_name>
    ```

1. Ensure your branch is up-to-date:

    ```bash
    git fetch --prune upstream
    git rebase upstream/master
    git push -f
    ```

1. Submit a [Pull Request](https://help.github.com/articles/using-pull-requests)
   - Participate in [code review](https://github.com/features/projects/codereview)
   - Participate in [code comments](https://github.com/blog/42-commit-comments)


License
-------

See LICENSE in this repo.


References
----------

* https://docs.docker.com/
* https://github.com/jpetazzo/nsenter
