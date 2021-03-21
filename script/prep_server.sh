#!/bin/bash

# Reference link
# https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04

echo 'Update server...'
sudo apt-get update -y && sudo apt-get upgrade -y

# Install Python
echo 'Installing Python...'
sudo apt-get install -y python3.8-dev \
                     python3.8-pip \
                     libmysqlclient-dev \
                     libpython3.8-dev \
                     nginx \
                     curl

# Install Pipenv
echo 'Install Pipenv...'
pip3 install pipenv --user
