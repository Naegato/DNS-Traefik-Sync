# DNS-Traefik-Sync

⚠️ only work on windows for now

## Problems :
- When you have a lot of services and, you want to manage them with Traefik, you have to write a lot of configuration in your dns (local or not).
- When you work with remote servers and Traefik you have to manage the dns of your services manually.
- I don't want to expose my home dns to the internet.

## Solution :

- This script will sync your Traefik configuration with your dns.

## How it works :

- The script will connect to your server in ssh and search all the containers running with Traefik labels that en by `.server.home`.
- It will then update your dns (hosts file) with the ip of the server.
- ***Disclaimer:*** the script need admin rights to edit the hosts file. It will ask for it, so don't panic !.

## How to use :

- You have to install the dependencies with `pip install -r requirements.txt`
- You have to configure the script with variables in the `.env` file.
- You have to run the script with `python3 main.py`

## Configuration :

- IP_ADDRESS : The ip address of your server.
- SSH_PORT : The ssh port of your server.
- USERNAME : The username of your server.
- WORKING_DIR : The working directory of your server.
- URL_REGEX : The regex to match the url of your services.
- HOSTS_FILE : The path to your hosts file.
- HOSTS_DELIMITER : The delimiter for sync in your hosts file.