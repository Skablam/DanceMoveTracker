#!/usr/bin/env bash

echo 'export DEBUG_ON=True' >> /home/vagrant/.bash_profile

cd /vagrant

source /vagrant/install.sh

gem install bundler

bundle install
