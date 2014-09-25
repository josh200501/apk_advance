#!/usr/bin/bash

while true;
do
    ps -ef |grep wget |wc -l
    sleep 1
done
