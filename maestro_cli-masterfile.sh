#sample commands to operate in EPAM Cloud
#docs
#https://cloud.epam.com/site/learn/quick_start/or2-quick-reference-card.pdf
#https://cloud.epam.com/site/learn/quick_start/csug_01_quick_start.pdf


#account setup
./or2access


#creates key pair
./or2-create-keypair -p personal -r epam-by2 -k semen_drobakha_epam_cloud_key_personal -s 4096


#for instances run
./or2-run-instances -p personal -r EPAM-BY2 -i CentOS7_64-bit -s MINI -c 2 -e 4H  -k semen_drobakha_epam_cloud_key_personal 2>/dev/null
#where
# -s MINI -> for 1 vcpu, 1GB RAM
# -c 2    -> count=2, launches 2 instances
# -e 4H   -> lunched for 4H and after will be stopped
# -k bla  -> ssh key name


#for instances termination
./or2-terminate-instances -p personal -r EPAM-BY2 -i <instance/id> -y


#some usage examples
./or2reboot -i <ID> -r epam-by2 -p personal  2>/dev/null 
./or2-describe-instances -r epam-by2 -p personal  2>/dev/null
./or2-stop ...
./or2start -i <ID> -r epam-by2 -p personal -e 4H  2>/dev/null


#connection example
ssh -i <path/to/key> 'name_name@epam.com'@hostname
