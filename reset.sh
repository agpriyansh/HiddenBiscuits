#!/bin/bash
while :
do
	rm -r database
    cp -r backup_database database
	sleep 1800
done
