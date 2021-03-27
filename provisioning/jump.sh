#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: jump.sh NODE"
    exit 1
fi

ip=$(yq -r .all.hosts."$1".ansible_host hosts.yml)
port=$(yq .all.vars.ansible_port hosts.yml)
key=$(yq -r .all.vars.ansible_ssh_private_key_file hosts.yml)

ssh -p "$port" -i "$key" root@"$ip"
