#!/usr/bin/env bash

sudo apt-get update

sudo apt-get install -y python-pip

sudo pip install -r /vagrant/requirements.txt 	

gem install bundler 

cd /vagrant

bundle install