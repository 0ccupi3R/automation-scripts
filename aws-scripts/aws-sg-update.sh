#!/bin/bash

# This script will be used with the arguments - PROTOCOL, PORT, PROFILE
# 
# Protocol  - all/tcp/udp
# Port      - 80/80-443/all
# Profile   - dev/stage/prod [optional]

#!/bin/bash
BOLD=`tput bold`
RED=`tput setaf 1`
YELLOW=`tput setaf 3`
DIM=`tput dim`
RESET=`tput sgr0`

if [ $# -eq 2 ]
then
    echo "Without Profile"
    ip=$(dig +short myip.opendns.com @resolver1.opendns.com.)
    aws ec2 authorize-security-group-ingress --group-name home-router --protocol $1 --port $2 --cidr $ip/32
else
    if [ $# -eq 3 ]
    then
        echo "With Profile"
        ip=$(dig +short myip.opendns.com @resolver1.opendns.com.)
        aws ec2 authorize-security-group-ingress --group-name home-router --protocol $1 --port $2 --cidr $ip/32 --profile $3
    else
            echo "${BOLD}${RED}Please provide the arguments [ protocol, port number, profile (optional) ]${RESET}\n${YELLOW}${DIM}aws-sg-update.sh <tcp/udp/all> <80/80-443/all> <dev/stage/prod>${RESET}\nExample: aws-sg-update.sh tcp 80 dev${RESET}\n"
    fi
fi
