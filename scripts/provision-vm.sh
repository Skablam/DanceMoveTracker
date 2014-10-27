#!/usr/bin/env bash

echo 'cd /vagrant' >> /home/vagrant/.bash_profile

echo 'export SETTINGS="config.DevelopmentConfig"' >> /home/vagrant/.bash_profile

#Run setup for each component in the environment
sh /vagrant/scripts/setup-python-ruby.sh
sh /vagrant/scripts/setup-postgres.sh
