#!/usr/bin/bash

echo "Update the repository and any packages..."
apt update && apt upgrade -y

echo "Install prerequisite system packages..."
apt install wget curl unzip jq -y

# Install Chromium
echo "deb http://deb.debian.org/debian/ sid main" >> /etc/apt/sources.list
apt-get update -qqy
apt-get -qqy install chromium
rm -rf /var/lib/apt/lists/* /var/cache/apt/*

# install chromedriver
apt-get update -qqy 
apt-get -qqy install chromium-driver 
rm -rf /var/lib/apt/lists/* /var/cache/apt/*
