#!/bin/bash
# jenkins adhoc related

ssh -i ${keyfile} -o StrictHostKeyChecking=no ${username}@${HOSTNAME} """
echo
echo "where am i"
echo
hostname
uname -a
ip addr show | grep inet | grep -v inet6

echo
echo "PWD"
echo
pwd
ls -la

echo
echo "who am i"
echo
whoami
"""
