VAGRANTFILE_API_VERSION = "2"

$script = <<SCRIPT
echo 'export DEBUG_ON=True' >> /home/vagrant/.bash_profile
echo 'export SETTINGS="config.DevelopmentConfig"' >> /home/vagrant/.bash_profile
SCRIPT

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "hashicorp/precise64"
  config.vm.synced_folder ".", "/home/vagrant/dancemovetracker", create: true
  config.vm.provision "shell", inline: $script
  config.vm.provision "shell", inline: "source /home/vagrant/dancemovetracker/install-postgres.sh"
  config.vm.provision "shell", inline: "source /home/vagrant/dancemovetracker/install.sh"

  config.vm.network "private_network", :ip => "172.16.42.43"
  config.vm.network "forwarded_port", guest: 8888, host: 8888
end
