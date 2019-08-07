#PUPPET INFRASTRUCTURE INSTALLATION


#1)--MASTER--
useradd sam
usermod -aG wheel sam
passwd sam
yum -y update
yum -y install vim htop git


rpm -ivh https://yum.puppetlabs.com/puppetlabs-release-el-7.noarch.rpm
yum -y install puppetserver


sed -i '/JAVA_ARGS=/s/=.*/= "-Xms512m -Xmx512m -XX:MaxPermSize=256m"/' /etc/sysconfig/puppetserver
vim /etc/puppetlabs/puppet/puppet.conf
 [main]
 certname = master.hostname
 server = master.hostname
 environment = production
 runinterval = 1h


systemctl start puppetserver
systemctl enable puppetserver

#FYI pin version is handy as during updates newer agents will not work with older master. not incluided here



#2)--AGENT--
useradd sam; 
usermod -aG wheel sam; 
passwd sam
yum -y update
yum -y install vim htop git


rpm -Uvh https://yum.puppetlabs.com/puppet5/puppet5-release-el-7.noarch.rpm
yum install -y puppet-agent


vim /etc/puppetlabs/puppet/puppet.conf
[main]
 certname = agent.hakase.io
 server = master.hakase.io
 environment = production
 runinterval = 1h


/opt/puppetlabs/bin/puppet resource service puppet ensure=running enable=true
systemctl start puppet


#3)--sign agent certificate on puppet master--
/opt/puppetlabs/bin/puppet cert list
/opt/puppetlabs/bin/puppet cert sign /ID/


#4)--directory environments and nodes match to environment--
--see hiera plugin--


