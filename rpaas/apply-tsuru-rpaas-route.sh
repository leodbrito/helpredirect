#!/bin/bash

set -eu

service="$1"
instance="$2"
real_address="$3"

green="\e[92m"
normal="\e[0m"

basedir=$(dirname $0)

echo
printf "${green}- Show current location config${normal}\n"
tsuru service-instance-info $service $instance

echo
printf "${green}- Apply new location config${normal}\n"
tsuru rpaas route -s $service -i $instance -p / -c "$(cat "$basedir/location.conf" |\
	    sed -e "s/%REAL_ADDRESS%/$real_address/g")" add

echo
printf "${green}- Review location config${normal}\n"
tsuru service-instance-info $service $instance