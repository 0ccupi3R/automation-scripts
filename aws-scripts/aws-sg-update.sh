#!/bin/bash

# This script will be used with the arguments - PROTOCOL, PORT, PROFILE
# 
# Protocol  - all/tcp/udp
# Port      - 80/80-443/all
# Profile   - dev/security/stage/prod

RED=`tput setaf 1`
YELLOW=`tput setaf 3`
RESET=`tput sgr0`

if [ $# -eq 3 ]
then
    ip=$(dig +short myip.opendns.com @resolver1.opendns.com.)
    aws ec2 authorize-security-group-ingress --group-name shahnawaz-home --protocol $1 --port $2 --cidr $ip/32 --profile $3
else
    echo "${YELLOW}Please provide three arguments -${RESET} ${RED}aws-sg-update.sh <tcp/udp/all> <80/80-443/all> <dev/security/prod>${RESET}"
fi
