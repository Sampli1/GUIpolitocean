#!/bin/bash

while true; do
    LC_NUMERIC="en_US.UTF-8"
    
    random_float=$(awk -v min=0 -v max=5 'BEGIN{srand(); printf "%.2f\n", min+rand()*(max-min)}')
    
    mosquitto_pub -t 'depth/' -h 127.0.0.1 -m "$random_float"
    
    sleep 1
done
