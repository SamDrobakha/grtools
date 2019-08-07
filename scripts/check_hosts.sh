#!/bin/bash
# Compares current IP with hosts file
# author Sam Drobakha

REAL_IP=$(hostname -i)
HOST=$(hostname)


IP_HOSTS=$(cat /etc/hosts | grep $HOST | awk {'print $1'})
if [ ${IP_HOSTS} == "${REAL_IP}" ] ; then
	echo "${IP} is set on ${HOST}"
        else
            echo "${IP} is NOT SET CORRECTLY in hosts file on ${HOST}"
fi

