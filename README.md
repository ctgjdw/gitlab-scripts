# Gitlab Management Scripts

This repository contains ansible scripts to manage `Gitlab` installations on `Docker`. The scripts can handle:

1. Backup and Upgrading of `Gitlab`
2. Restoring backups **TODO**
3. Scheduling backups via crontab **TODO**

## To Run

You may run the script via the `docker-compose.yml` file. It uses the `cytopia/ansible:2.13-tools` ansible docker image to run the ansible script against your `Docker`/`Docker Swarm Manager` node.

This ansible container should have network access to your node, as it uses `SSH` to propogate the instructions.

> The script will also need an ssh key to access your node

## Backup and Upgrading of Gitlab

1. Edit `hosts.yml`
   1. `<HOST_IP>`: Replace this with the address of your `Docker`/`Docker Swarm Manager` node
   2. `<USER>`: Replace this with the user's username of your `Docker`/`Docker Swarm Manager` node
2. Add the private key for your `SSH` key named `key.pem` into the root directory of this repo
3. Build the image - `docker compose build`
4. Run the `upgrade-gitlab` script - `docker compose run upgrade-gitlab`
5. Enter the following into the script's prompts:
   1. Docker Swarm Gitlab service name: The name of your docker service (from Portainer/`docker service ls`)
   2. The current Gitlab image tag: e.g. `docker.io/gitlab/gitlab-ce:16.2.2-ce.0`
   3. The target Gitlab image tag to upgrade to: e.g. `docker.io/gitlab/gitlab-ce:16.8.0-ce.0`

> Note: the script will only update the `Docker Swarm` service to use the target image. After all upgrades are complete, you **will** need to **manually update** your `Docker Swarm Stack`/`docker-compose.yml` definition to use the target image.
