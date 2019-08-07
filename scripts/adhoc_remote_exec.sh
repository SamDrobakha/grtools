#!/bin/bash
#adhoc commands execution on remote boxes
#author Sam Drobakha


HOSTS=($(cat inventory_adhoc))
login=thelogin
passw=lalala


for host in ${HOSTS[@]}; do
	echo "Working on host ${host}"
	sshpass -p "$passw" ssh -t -q -o StrictHostKeyChecking=no ${login}@${host} \
    #ADD COMMANDS HERE
    "
    uptime

    "
done


