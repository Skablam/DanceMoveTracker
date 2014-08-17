#!/usr/bin/env bash

echo 'cd /vagrant' >> /home/vagrant/.bash_profile

echo 'export SETTINGS="config.DevelopmentConfig"' >> /home/vagrant/.bash_profile

#Run setup for each component in the environment
sh /vagrant/Provision-Scripts/setup-python-ruby.sh
sh /vagrant/Provision-Scripts/setup-postgres.sh
