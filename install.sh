sudo apt-get update

#install packages required for python libraries
sudo apt-get install -y python-dev

sudo apt-get install -y libpq-dev

sudo apt-get install -y python-pip

dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $dir

#install python libraries
sudo pip install -r requirements.txt

#install sass
gem install bundler

bundle install

#install and configure supervisor
sudo apt-get install -y supervisor

echo "[program:dancemovetracker]
command=gunicorn --log-file=- --log-level DEBUG -b 0.0.0.0:8888 --timeout 120 application.server:app
directory=$dir
autostart=true
autorestart=true" > /etc/supervisor/conf.d/dancemovetracker.conf
