Overview
--------

This repo contains scripts and source to build multiple docker images
with Alpine Linux. The main application container has a LAMP stack of:

* Apache
* MySQL
* PHP
* Python

Build status on CircleCI (master branch): [![Circle CI](https://circleci.com/gh/ISEexchange/tacstack/tree/master.svg?style=svg&circle-token=373b7a10221a0403c993da96c45ba15ef225e932)](https://circleci.com/gh/ISEexchange/tacstack/tree/master)


Build and Deploy locally with docker-compose
-------------

docker-compose will provide a fully functioning MAP system
from scratch. It will build all of the required images and start up
the containers. It will also take care of linking the data and app
containers and will provide ports for you to use. Use this to create
either a test environment or a production environment. To get started,
clone this git repo, then run:

    docker-compose up -d

The `-d` will start the applications in the background.

The ports for the internal applications will be randomly
selected. To find them, run:

    docker-compose ps

The ports will be listed under the mapapp container.

There are four services in this system that docker-compose will bring up:

    mapapp
    ftpapp
    mysqldatavol
    ftpdatavol

For more information on docker-compose:
https://docs.docker.com/compose/


Build on CircleCI
-----------------

Open a pull request on Github.
This triggers a build in CircleCI.
At the moment, this will only build the main docker application.
docker-compose integration with CircleCI coming soon.


Build locally with docker
-------------

To build the main application container, clone this git
repo, then run:

    script/build


Manual Deployment
----------

Follow these instructions if you are not using docker-compose.
For a live TAC application, run:

```
docker run -d -p 2222:22 -p 80:80 quay.io/iseexchange/tacstack
```

For an individual test environment, run:

```
CID=$(docker run -d -P quay.io/iseexchange/tacstack)

# Find the port on which sshd is running.
docker port $CID 22

# Find the port on which apache is running.
docker port $CID 80
```


Troubleshooting
---------------

### Outside a container

```bash
# Commands for docker-compose:
# List active and exited containers.
docker-compose ps
# Follow logs from a container.
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
