Overview
--------

This repo contains scripts and source to build a docker image
with CentOS 6.5 and a LAMP stack of:

* Apache
* MySQL
* PHP
* Python


Deployment
----------

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
# List active containers.
docker ps

# List all containers.
docker ps -a

# Follow logs from a container.
docker logs -f <container-id>

# Get help.
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


OVAL vulnerability scan
-----------------------

The docker build runs a vulnerability scan.
You can also perform the scan inside an existing build via:

    docker run --rm -t quay.io/iseexchange/tacstack /oval/vulnerability-scan.sh

See https://github.com/jumanjihouse/oval for details.

TODO: Implement some sort of CD system to poll the OVAL feed and rebuild
the image on any update. https://github.com/jumanjiman/docker-gocd may be
a candidate for the solution.


Contributing
------------

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
