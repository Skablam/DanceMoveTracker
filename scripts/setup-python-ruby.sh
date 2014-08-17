#!/usr/bin/env bash

echo 'export DEBUG_ON=True' >> /home/vagrant/.bash_profile

sudo apt-get update

sudo apt-get install -y python-dev

sudo apt-get install -y libpq-dev

sudo apt-get install -y python-pip

sudo pip install -r /vagrant/requirements.txt

gem install bundler

cd /vagrant

bundle install
