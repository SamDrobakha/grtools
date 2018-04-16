Description: This soution builds reliable FTP service using Amazon S3 bucket as a storage
Inspired by: https://cloudacademy.com/blog/s3-ftp-server/

This manual assumes you have AWS CLI configured, if not, please do it.

1. create t2.micro instance ans assign keys (vps, security group, igw were already there)
2. EIP
3. route53 A entry

4. ec2 work:
#[S3FS-FUSE]
sudo yum -y update
sudo yum -y install git automake make gcc libstdc++-devel gcc-c++ fuse fuse-devel libcurl-devel curl-devel libxml2-devel mailcap openssl-devel

mkdir ~/misc && cd ~/misc
git clone https://github.com/s3fs-fuse/s3fs-fuse.git
cd s3fs-fuse
./autogen.sh
./configure
make
sudo make install
#[VSFTPD]
sudo yum -y install vsftpd
#[FTPS]
sudo mkdir -p /etc/ssl/private
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/vsftpd.pem -out /etc/ssl/private/vsftpd.pem
sudo vi /etc/vsftpd/vsftpd.conf
sudo cp /etc/vsftpd/vsftpd.conf /etc/vsftpd/vsftpd.conf.origin
sudo vi /etc/vsftpd/vsftpd.conf
------------------------------------------
anonymous_enable=NO
local_enable=YES
chroot_local_user=YES
tcp_wrappers=YES
write_enable=YES
allow_writeable_chroot=YES

userlist_enable=YES
userlist_file=/etc/vsftpd.userlist
userlist_deny=NO

pasv_enable=yes
pasv_min_port=15390 
pasv_max_port=15690 
pasv_address=18.197.127.113
listen_port=15400

rsa_cert_file=/etc/ssl/private/vsftpd.pem
rsa_private_key_file=/etc/ssl/private/vsftpd.pem

ssl_enable=YES
allow_anon_ssl=NO
force_local_data_ssl=YES
force_local_logins_ssl=YES

ssl_tlsv1=YES
ssl_sslv2=NO
ssl_sslv3=NO

require_ssl_reuse=NO
ssl_ciphers=HIGH
-------------------------------------
#[S3 MOUNT]
sudo mkdir -p /mnt/s3fs-001-grtools-cc
#[add role] with policy like "AmazonS3FullAccess" to your ec2 instance
sudo vi /etc/fuse.conf
#uncomment user_allow_other
#create bucket "s3fs-001-grtools-cc" or choose exisiting one. Don't add dots in bucket name.
sudo /usr/local/bin/s3fs s3fs-001-grtools-cc /mnt/s3fs-001-grtools-cc -o iam_role -o allow_other
#[FSTAB]
sudo vi /etc/fstab
s3fs-001-grtools-cc /mnt/s3fs-001-grtools-cc fuse.s3fs _netdev,allow_other,iam_role 0 0

#[SECURITY GROUP]dont forget to allow inbound traffic to 990/tcp, 15390:15690/tcp
#[VSFTPD: USER]
sudo useradd -d /mnt/s3fs-001-grtools-cc -s /sbin/nologin ftpuser1
sudo passwd ftpuser1
sudo vi /etc/vsftpd.userlist
#add ftpuser1
sudo systemctl restart vsftpd
sudo systemctl enable vsftpd


#[testing]5. test connection to s3 from ec2
#aws s3 sync ~/misc s3://s3fs-001-grtools-cc
#aws s3 ls s3://s3fs-001-grtools-cc
#aws s3 rm s3://s3fs-001-grtools-cc --recursive

#[testing]6.1. test it
#ls / > /mnt/s3fs-001-grtools-cc/testfile
#aws s3 ls s3://s3fs-001-grtools-cc
#rm /mnt/s3fs-001-grtools-cc/testfile

#[TESTING]8. FTP testing
#sudo yum -y install ftp
#ftp -p 127.0.0.1

#[FileZilla] Status:	Server sent passive reply with unroutable address. Using server address instead.


9. references:
https://cloudacademy.com/blog/s3-ftp-server/
https://github.com/s3fs-fuse/s3fs-fuse
https://github.com/s3fs-fuse/s3fs-fuse/issues/602
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html
https://www.digitalocean.com/community/tutorials/how-to-set-up-vsftpd-for-a-user-s-directory-on-ubuntu-16-04
https://stackoverflow.com/questions/7052875/setting-up-ftp-on-amazon-cloud-server